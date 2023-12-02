import pymem.exception
from save import *
from pymem import Pymem
import time
from datetime import datetime

saveStructure = loadData()

def readAnimalNameFromPointer(harvest_base_address):
    # Animal names are sometimes stored as address pointers to strings... White-Tailed Jackrabbit is such instance.
    try:
        animalName = pm.read_string(pm.read_longlong(harvest_base_address), 32)
        return animalName
    except UnicodeDecodeError:
        print("Failed to read animal\'s name. Please raise an issue in the GitHub repo with the animal you have harvested for a potential fix. Thank you.")
        return None

def getHarvestBaseAddress(pm):
    print("Searching for harvest base address...")
    harvest_base_address = pm.pattern_scan_module(b"\x48\x83\x3D....\x00\x74.\xC7\x45\x10....\x48\x8D\x55\x10\x48\x8B\x0D....\xE8....\x48\x85\xC0\x74\x0D\x8B\x80\xB4\x00\x00\x00\xFF\xC8\x83\xF8\x01\x76\x48", "theHunterCotW_F.exe")

    if harvest_base_address is None:
        print(">>> Harvest base address not found, are you running the correct game version?")
        input("Press Enter to close... ")
        exit(0)

    harvest_base_address += 0x03
    harvest_base_address = pm.read_int(harvest_base_address) + harvest_base_address + 0x05
    harvest_base_address = pm.read_longlong(harvest_base_address) + 0x280

    print("Harvest base address is at " + hex(harvest_base_address))
    return harvest_base_address


def getSessionScoreAddress(pm):
    print("Searching for session score address...")
    session_score_address = pm.pattern_scan_module(b"\x48\x8B\x05....\x48\x8B\x70\x60\x48\x85\xF6\x74\x33", "theHunterCotW_F.exe")

    if session_score_address is None:
        print(">>> Session score address not found, are you running the correct game version?")
        input("Press Enter to close... ")
        exit(0)

    session_score_address += 0x03
    session_score_address = pm.read_int(session_score_address) + session_score_address + 0x04
    session_score_address = pm.read_longlong(session_score_address)+0x40

    session_score_address = pm.read_longlong(pm.read_longlong(pm.read_longlong(session_score_address))+0x190)

    session_score_address += 0x6B0

    print("Session score address is at " + hex(session_score_address))
    return session_score_address


def getFurTypeBaseAddress(pm):
    print("Searching for fur type base address...")
    fur_type_base_address = pm.pattern_scan_all(b"\x5A\xAA\xFA\x11\x32\x33\x00\x00")

    if fur_type_base_address is None:
        print(">>> Fur type address not found, are you running the correct game version?")
        input("Press Enter to close... ")
        exit(0)

    fur_type_base_address -= 0x2C8

    print("Fur type base address is at " + hex(fur_type_base_address))
    return fur_type_base_address


def getFurTypeBaseAddress2(pm):
    print("Searching for fur type base address 2...")
    fur_type_base_address2 = pm.pattern_scan_all(b"\xB3\x59\x17\xE9\x8B\x72\x13\x00")

    if fur_type_base_address2 is None:
        print(">>> Fur type address 2 not found, are you running the correct game version?")
        input("Press Enter to close... ")
        exit(0)

    fur_type_base_address2 -= 0x1F368
    fur_type_base_address2 -= 0x3E8

    print("Fur type base address 2 is at " + hex(fur_type_base_address2))
    return fur_type_base_address2


def getFurTypeName(fur_type_offset, fur_type_base_address, fur_type_base_address2, pm):
    # By the looks of it, that's where the array has ended... although it may contain more than what we need, we should be fine.
    max_iteration_count = 690
    fur_type_iterator = fur_type_base_address + 0x150

    try:
        while max_iteration_count > 0:
            current_fur_type = pm.read_int(fur_type_iterator)

            if current_fur_type == fur_type_offset:
                name_address = pm.read_longlong(fur_type_base_address)
                # Add translation offset to name address.
                name_address += pm.read_int(fur_type_iterator + 0x04)
                return pm.read_string(name_address)

            # Add 8 bytes and scan again.
            fur_type_iterator += 0x08
            max_iteration_count = max_iteration_count - 1

        max_iteration_count = 0x030000
        fur_type_iterator = fur_type_base_address2 + 0x110

        while max_iteration_count > 0:
            current_fur_type = pm.read_int(fur_type_iterator)

            if current_fur_type == fur_type_offset:
                name_address = pm.read_longlong(fur_type_base_address2)
                # Add translation offset to name address.
                name_address += pm.read_int(fur_type_iterator + 0x04)
                return pm.read_string(name_address)

            # Add 8 bytes and scan again.
            fur_type_iterator += 0x08
            max_iteration_count = max_iteration_count - 1
    except UnicodeDecodeError:
        print("Failed to determine animal fur type name. Please report this on GitHub with the following type offset: "+str(fur_type_offset))

    return "UNKNOWN"


try:
    print("- CotW Harvest Tracker v1.14 -")

    print("Searching for theHunterCotW_F process...")
    pm = Pymem('theHunterCotW_F.exe')

    session_score_address = getSessionScoreAddress(pm)
    harvest_base_address = getHarvestBaseAddress(pm)
    fur_type_base_address = getFurTypeBaseAddress(pm)
    fur_type_base_address2 = getFurTypeBaseAddress2(pm)

    if harvest_base_address is not None:
        latestKillRecordAnswer = input("Would you like to record your latest kill which happened before starting this program? y/n: ")

        if str.lower(latestKillRecordAnswer) == "y":
            lastHarvestWeight = 0
            lastSessionScore = 0
            print("Latest kill will be recorded.")
        else:
            lastHarvestWeight = pm.read_float(harvest_base_address + 0x24)
            lastSessionScore = pm.read_int(session_score_address)
            print("Latest kill was not recorded.")


        print("- All is good, we are checking your harvest every second -")
        harvestedAnimalIDs = []

        while True:
            time.sleep(1)

            try:
                try:
                    newHarvestWeight = pm.read_float(harvest_base_address+0x24)
                except pymem.exception.MemoryReadError:
                    print(" > Failed to read process memory. Have you closed the game? <")
                    input("Press Enter to close... ")
                    exit(0)

                newSessionScore = pm.read_int(session_score_address)

                # Session score has changed.
                if newSessionScore != lastSessionScore:
                    # Harvest weight has changed.
                    if newHarvestWeight != lastHarvestWeight:
                        # Try to determine animal name.
                        try:
                            animalName = pm.read_string(harvest_base_address, 32)

                            if animalName not in saveStructure.animals:
                                animalName = readAnimalNameFromPointer(harvest_base_address)
                                if animalName is None:
                                    print("Failed to read animal name. (1)")
                                    continue

                        except UnicodeDecodeError:
                            animalName = readAnimalNameFromPointer(harvest_base_address)
                            if animalName is None:
                                print("Failed to read animal name. (2)")
                                continue

                        newAnimal = AnimalData(newHarvestWeight, pm.read_int(harvest_base_address+0x20), pm.read_int(harvest_base_address+0XB0), pm.read_float(harvest_base_address+0X3C), pm.read_int(harvest_base_address+0X38), pm.read_int(harvest_base_address+0X34), pm.read_int(harvest_base_address+0XAC), pm.read_float(harvest_base_address+0X40), datetime.now().strftime("%Y/%m/%d %H:%M:%S"), getFurTypeName(pm.read_int(harvest_base_address+0x50), fur_type_base_address, fur_type_base_address2, pm))

                        newAnimalID = newAnimal.getID()

                        if newAnimalID not in harvestedAnimalIDs:
                            harvestedAnimalIDs.append(newAnimalID)
                            print("["+str(len(harvestedAnimalIDs))+"] "+animalName+" - "+newAnimal.toString())
                            lastHarvestWeight = newHarvestWeight
                            lastSessionScore = newSessionScore
                            saveStructure.animals[animalName].append(newAnimal)
                            saveData(saveStructure)
                        else:
                            print("Animal has already been harvested: "+newAnimalID)

            except Exception as e:
                print("Exception!")
                print(e)

    else:
        print("Failed to determine harvest base address, the game version might have changed.")

except pymem.exception.ProcessNotFound:
    print("Failed to attach to theHunterCotW_F process, please start the game before starting this app.")

input("Press Enter to close... ")
