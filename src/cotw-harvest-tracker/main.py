import pymem.exception
from save import *
from pymem import Pymem
import sys, time
from datetime import datetime
import msvcrt

class CotWHarvestTracker:
    def __init__(self):
        print("- CotW Harvest Tracker v1.18 -")
        print("INFO: Initializing...")
        self.harvested_animal_ids = []
        self.save_structure = loadData()
        try:
            self.pm = Pymem('theHunterCotW_F.exe')
        except:
            self.report_error_and_quit("Failed to attach to game\'s memory process, please start the game before starting this app")
        
        self.set_game_addresses()
        self.get_latest_harvest()

        self.run_harvest_checker()

    def report_ok(self):
        print("- All is good, we are checking your harvest every second -")
        return None

    def report_error_and_quit(self, error=None, ticket=False, quit=True):
        # Error message
        error_message = "ERROR: Exception! "
        if error is not None:
            error_message += str(error)
        print(error_message)

        # Create repo issue ticket
        if ticket:
            print("INFO: Please create an issue ticket on GitHub repo, include error message and steps to replicate, via:\nhttps://github.com/LordHansCapon/cotw-harvest-tracker/issues")
        
        # Quit
        if quit:
            input("INPUT: Press any key to close...")
            sys.exit(1)

        return None

    def set_game_addresses(self):
        try:
            self.session_score_address = self.get_session_score_address()
            print("INFO: Obtained session score address:\t" + hex(self.session_score_address))

            self.harvest_base_address = self.get_harvest_base_address()
            print("INFO: Obtained harvest base address:\t" + hex(self.harvest_base_address))

            self.fur_type_base_address = self.get_fur_type_base_address()
            print("INFO: Obtained fur type base address:\t" + hex(self.fur_type_base_address))

            self.fur_type_base_address_2 = self.get_fur_type_base_address_2()
            print("INFO: Obtained fur type base address 2:\t" + hex(self.fur_type_base_address_2))

            return None

        except Exception as e:
            self.report_error_and_quit("Failed to initialize memory addresses, please start the game before starting this app")

    def get_session_score_address(self):
        session_score_address = self.pm.pattern_scan_module(b"\x48\x8B\x05....\x48\x8B\x70\x60\x48\x85\xF6\x74\x33", "theHunterCotW_F.exe")

        if session_score_address is None:
            self.report_error_and_quit("Session score address not found, please verify game is up to date")

        session_score_address += 0x03
        session_score_address = self.pm.read_int(session_score_address) + session_score_address + 0x04
        session_score_address = self.pm.read_longlong(session_score_address) + 0x40

        session_score_address = self.pm.read_longlong(self.pm.read_longlong(self.pm.read_longlong(session_score_address)) + 0x190)
        session_score_address += 0x6B0

        return session_score_address

    def get_harvest_base_address(self):
        harvest_base_address = self.pm.pattern_scan_module(b"\x48\x83\x3D....\x00\x74.\xC7\x45\x10....\x48\x8D\x55\x10\x48\x8B\x0D....\xE8....\x48\x85\xC0\x74\x0D\x8B\x80\xB4\x00\x00\x00\xFF\xC8\x83\xF8\x01\x76\x48", "theHunterCotW_F.exe")

        if harvest_base_address is None:
            self.report_error_and_quit("Harvest base address not found, please verify game is up to date")

        harvest_base_address += 0x03
        harvest_base_address = self.pm.read_int(harvest_base_address) + harvest_base_address + 0x05
        harvest_base_address = self.pm.read_longlong(harvest_base_address) + 0x280

        return harvest_base_address

    def get_fur_type_base_address(self):
        fur_type_base_address = self.pm.pattern_scan_all(b"\x5A\xAA\xFA\x11\x32\x33\x00\x00")

        if fur_type_base_address is None:
            self.report_error_and_quit("Fur type address not found, please verify game is up to date")

        fur_type_base_address -= 0x2C8

        return fur_type_base_address

    def get_fur_type_base_address_2(self):
        fur_type_base_address_2 = self.pm.pattern_scan_all(b"\xB3\x59\x17\xE9\x8B\x72\x13\x00")

        if fur_type_base_address_2 is None:
            self.report_error_and_quit("Fur type address 2 not found, please verify game is up to date")

        fur_type_base_address_2 -= 0x1F740

        return fur_type_base_address_2

    def get_latest_harvest(self):
        if self.harvest_base_address is not None:
            print("INPUT: Would you like to record your latest kill which happened before starting this program? (y/n): ", end='', flush=True)
            start_time = time.time()

            while True:
                if msvcrt.kbhit():
                    latest_harvest_answer = msvcrt.getch().decode()
                    print()
                    break
                if time.time() - start_time > 30:   # Continue after 30 sec if no input entered
                    latest_harvest_answer = "n"
                    print("\nINFO: No input entered, continuing...")
                    break

            self.check_and_set_new_session()    # Make sure session is current before continuing
            if str.lower(latest_harvest_answer) == "y":
                self.last_harvest_weight = 0
                self.last_session_score = 0
                print("INFO: Latest kill will be recorded...")
            else:
                self.last_harvest_weight = self.pm.read_float(self.harvest_base_address + 0x24)
                self.last_session_score = self.pm.read_int(self.session_score_address)
                print("INFO: Latest kill was NOT recorded")
        else:
            self.report_error_and_quit("Failed to determine harvest base address")

        return None

    def check_and_set_new_session(self):
        try:
            current_session_score_address = self.get_session_score_address()
            if current_session_score_address != self.session_score_address:
                time.sleep(1)   # Wait for address to fully initialize
                self.session_score_address = self.get_session_score_address()
                print("INFO: Detected new session address:\t{}".format(hex(self.session_score_address)))
                self.report_ok()

            return None

        except Exception as e:
            self.report_error_and_quit("Unable to check and set session, have you closed the game?")

    def read_animal_name_from_pointer(self):
        # Animal names are sometimes stored as address pointers to strings... White-Tailed Jackrabbit is such instance.
        try:
            animal_name = self.pm.read_string(self.pm.read_longlong(self.harvest_base_address), 32)
            return animal_name
        except Exception as e:
            self.report_error_and_quit("Failed to read animal\'s name", True, False)
            return None

    def get_fur_type_name(self, fur_type_offset):
        # By the looks of it, that's where the array has ended... although it may contain more than what we need, we should be fine.
        max_iteration_count = 690
        fur_type_iterator = self.fur_type_base_address + 0x150

        try:
            while max_iteration_count > 0:
                current_fur_type = self.pm.read_uint(fur_type_iterator)

                if current_fur_type == fur_type_offset:
                    name_address = self.pm.read_longlong(self.fur_type_base_address)
                    # Add translation offset to name address
                    name_address += self.pm.read_uint(fur_type_iterator + 0x04)
                    return self.pm.read_string(name_address)

                # Add 8 bytes and scan again.
                fur_type_iterator += 0x08
                max_iteration_count = max_iteration_count - 1

            max_iteration_count = 0x030000
            fur_type_iterator = self.fur_type_base_address_2 + 0x160

            while max_iteration_count > 0:
                current_fur_type = self.pm.read_uint(fur_type_iterator)

                if current_fur_type == fur_type_offset:
                    name_address = self.pm.read_longlong(self.fur_type_base_address_2)
                    # Add translation offset to name address
                    name_address += self.pm.read_uint(fur_type_iterator + 0x04)
                    return self.pm.read_string(name_address)

                # Add 8 bytes and scan again
                fur_type_iterator += 0x08
                max_iteration_count = max_iteration_count - 1

        except Exception as e:
            self.report_error_and_quit("Failed to determine animal fur type name, include offset in ticket: " + str(hex(fur_type_offset)), True, False)

        return "UNKNOWN"

    def run_harvest_checker(self):
        self.report_ok()

        while True:
            time.sleep(1)
            try:
                self.check_and_set_new_session()
                self.check_harvest()
            except Exception as e:
                self.report_error_and_quit(e, True)

    def check_harvest(self):
        try:
            try:
                new_harvest_weight = self.pm.read_float(self.harvest_base_address + 0x24)
            except Exception as e:
                self.report_error_and_quit("Failed to read process memory, have you closed the game?")

            new_session_score = self.pm.read_int(self.session_score_address)

            # Session score has changed
            if new_session_score != self.last_session_score:
                # Harvest weight has changed
                if new_harvest_weight != self.last_harvest_weight:
                    # Try to determine animal name
                    try:
                        animal_name = self.pm.read_string(self.harvest_base_address, 32)

                        if animal_name not in self.save_structure.animals:
                            animal_name = self.read_animal_name_from_pointer()
                            if animal_name is None:
                                self.report_error_and_quit("Failed to read animal name (1)", True, False)

                    except Exception as e:
                        animal_name = self.read_animal_name_from_pointer()
                        if animal_name is None:
                            self.report_error_and_quit("Failed to read animal name (2)", True, False)

                    new_animal = AnimalData(new_harvest_weight, int.from_bytes(self.pm.read_bytes(self.harvest_base_address + 0x20, 1), "big"), self.pm.read_int(self.harvest_base_address + 0XB0), self.pm.read_float(self.harvest_base_address + 0X3C), self.pm.read_int(self.harvest_base_address + 0X38), self.pm.read_int(self.harvest_base_address + 0X34), int.from_bytes(self.pm.read_bytes(self.harvest_base_address + 0xAC, 1), "big"), self.pm.read_float(self.harvest_base_address + 0X40), datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.get_fur_type_name(self.pm.read_uint(self.harvest_base_address + 0x50)))

                    new_animal_id = new_animal.getID()

                    if new_animal_id not in self.harvested_animal_ids:
                        self.harvested_animal_ids.append(new_animal_id)
                        print("[{}] {} - {}".format(str(len(self.harvested_animal_ids)), animal_name, new_animal.toString()))
                        self.last_harvest_weight = new_harvest_weight
                        self.last_session_score = new_session_score
                        self.save_structure.animals[animal_name].append(new_animal)
                        saveData(self.save_structure)
                    else:
                        print("INFO: Animal has already been harvested: " + new_animal_id)

        except Exception as e:
            self.report_error_and_quit(e, True)

if __name__ == "__main__":
    CotWHarvestTracker()
