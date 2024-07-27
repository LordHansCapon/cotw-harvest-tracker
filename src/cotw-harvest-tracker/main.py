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
    harvest_base_address = pm.read_longlong(harvest_base_address) + 0x288

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


def getHarvestFurName(pm):
    try:
        return pm.read_string(pm.read_longlong(fur_name_pointer_cache_address))
    except Exception:
        print("Failed to read animal\'s fur. UNKNOWN is set.")
        return "UNKNOWN"
    except UnicodeDecodeError:
        print("Failed to read animal\'s fur. UNKNOWN is set.")
        return "UNKNOWN"

try:
    print("- CotW Harvest Tracker v1.18 -")

    print("Searching for theHunterCotW_F process...")
    pm = Pymem('theHunterCotW_F.exe')
    print("Base address: "+str(hex(pm.base_address)))

    fur_name_pointer_cache_address = pm.allocate(0x08)
    fur_cache_function_address = pm.allocate(0x10)

    #print("fur_name_pointer_cache_address: "+str(hex(fur_name_pointer_cache_address)))
    #print("fur_cache_function_address: "+str(hex(fur_cache_function_address)))

    fur_type_detour_address = pm.pattern_scan_all(b"\x45\x33\xC9\x41\xB0\x01\x41\x8B\x96\xD8\x02\x00\x00\x48\x8B\x0D")
    fur_type_detour_address += 54
    #print("fur_type_detour_address: "+str(hex(fur_type_detour_address)))

    # Fur cache function.
    pm.write_bytes(fur_cache_function_address, b"\x50\x48\xB8", 3)
    pm.write_bytes(fur_cache_function_address+3, int.to_bytes(fur_name_pointer_cache_address, 8, byteorder="little"), 8)
    pm.write_bytes(fur_cache_function_address+11, b"\x4C\x89\x08", 3)
    pm.write_bytes(fur_cache_function_address+14, b"\x58", 1)
    pm.write_bytes(fur_cache_function_address+15, b"\xC3", 1)

    # Fur type detour to fur cache function.
    pm.write_bytes(fur_type_detour_address, b"\xFF\x15\x02\x00\x00\x00\xEB\x08", 8)
    pm.write_bytes(fur_type_detour_address+8, int.to_bytes(fur_cache_function_address, 8, byteorder="little"), 8)
    pm.write_bytes(fur_type_detour_address+16, b"\x90\x90", 2)

    session_score_address = getSessionScoreAddress(pm)
    harvest_base_address = getHarvestBaseAddress(pm)

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

                        newAnimal = AnimalData(newHarvestWeight, int.from_bytes(pm.read_bytes(harvest_base_address+0x20, 1), "big"), pm.read_int(harvest_base_address+0XB0), pm.read_float(harvest_base_address+0X3C), pm.read_int(harvest_base_address+0X38), pm.read_int(harvest_base_address+0X34), int.from_bytes(pm.read_bytes(harvest_base_address+0xAC, 1), "big"), pm.read_float(harvest_base_address+0X40), datetime.now().strftime("%Y/%m/%d %H:%M:%S"), getHarvestFurName(pm))

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
