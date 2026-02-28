import pymem.exception
import time
import os
import traceback
import pyautogui, pygetwindow, pyscreeze
from scanner import *
from datetime import datetime
from save import *
from logger import *
from pymem import Pymem
from pymem.ressources.kernel32 import VirtualProtectEx
from ctypes import c_void_p, c_ulong

saveStructure = loadData()


def getRatingLevelFromText(ratingLevelText):
    match ratingLevelText:
        case "diamond":
            return 0
        case "gold":
            return 1
        case "silver":
            return 2
        case "bronze":
            return 3
        case "none":
            return 4
        # Added later so they done goofed the enum.
        case "greatone":
            return 5

    return 4


def readAnimalNameFromHarvest(harvest_base_address):
    # Animal names are sometimes stored as address pointers to strings... White-Tailed Jackrabbit is such instance.
    try:
        animalName = pm.read_string(pm.read_longlong(harvest_base_address), 32)
        # Just in case. Since they done goofed with the location names.
        animalName = animalName.rstrip()
        return animalName
    except:
        pass

    try:
        animalName = pm.read_string(harvest_base_address, 32)
        animalName = animalName.rstrip()
        return animalName
    except:
        logError(
            "Failed to read animal\'s name. Please raise an issue in the GitHub repo with the animal you have harvested for a potential fix. Thank you.")
        return None


def readLocationNameFromHarvest(harvest_base_address):
    # Location names are sometimes stored as address pointers to strings...
    try:
        locationName = pm.read_string(pm.read_longlong(harvest_base_address + 0x60), 32)
        # Really... some locations have extra spaces at the end for some reason.
        locationName = locationName.rstrip()
        return locationName
    except:
        pass

    try:
        locationName = pm.read_string(harvest_base_address + 0x60, 32)
        # Really... some locations have extra spaces at the end for some reason.
        locationName = locationName.rstrip()
        return locationName
    except UnicodeDecodeError:
        logError(
            "Failed to read location\'s name. Please raise an issue in the GitHub repo with the location you have harvested in for a potential fix. Thank you.")
        return None


def writeHarvestDetour(pm):
    harvest_detour_target_bytes = b"\x0F\xB6\x45\xD0\x88\x43\x20\x0F\x10\x45\xD4\x0F\x11\x43\x24"

    # +BA22CE in current game version (movzx eax,byte ptr [rbp-30])
    harvest_address_detour_address = scan_process(pm, harvest_detour_target_bytes)[0]
    logInfo("Harvest detour address: " + str(hex(harvest_address_detour_address)))
    trampoline_size = len(harvest_detour_target_bytes)

    old_protect = c_ulong()
    VirtualProtectEx(pm.process_handle, c_void_p(harvest_address_detour_address), trampoline_size, 0x40, old_protect)

    harvest_base_address = pm.allocate(0x08)
    harvest_base_address_detour_fn = pm.allocate(0x80)
    logInfo("Detour fn address: " + str(hex(harvest_base_address_detour_fn)))

    stolen_bytes = pm.read_bytes(harvest_address_detour_address, trampoline_size)
    pm.write_bytes(harvest_base_address_detour_fn, stolen_bytes, len(stolen_bytes))

    # Store base harvest address
    pm.write_bytes(harvest_base_address_detour_fn + len(stolen_bytes),
                   b"\x48\xB8" + int.to_bytes(harvest_base_address, 8, "little") + b"\x48\x89\x18", 13)

    # Return
    pm.write_bytes(harvest_base_address_detour_fn + len(stolen_bytes) + 13, b"\xC3", 1)

    trampoline = b"\x50\x48\xB8" + harvest_base_address_detour_fn.to_bytes(8, "little") + b"\xFF\xD0\x58\x90"
    pm.write_bytes(harvest_address_detour_address, trampoline, len(trampoline))
    VirtualProtectEx(pm.process_handle, c_void_p(harvest_address_detour_address), trampoline_size, old_protect.value,
                     c_ulong())
    return harvest_base_address


def writeHarvestFurDetour(pm):
    fur_detour_target_bytes = b"\x44\x8B\x81\xD0\x00\x00\x00\x41\x8B\x96\xE0\x02\x00\x00\xE8"

    # +BC0EEB in current game version (mov r8d,[rcx+000000D0])
    fur_detour_address = scan_process(pm, fur_detour_target_bytes)[0]
    fur_detour_address = fur_detour_address + len(fur_detour_target_bytes) + 0x04
    logInfo("Fur detour address: " + str(hex(fur_detour_address)))
    trampoline_size = 14

    old_protect = c_ulong()
    VirtualProtectEx(pm.process_handle, c_void_p(fur_detour_address), trampoline_size, 0x40, old_protect)

    harvest_fur_address = pm.allocate(0x08)
    harvest_fur_address_detour_fn = pm.allocate(0x80)
    logInfo("Fur detour fn address: " + str(hex(harvest_fur_address_detour_fn)))

    target_addr = fur_detour_address + 7 + int.from_bytes(pm.read_bytes(fur_detour_address + 3, 4), "little",
                                                          signed=True)
    base_bytes = b"\x49\xB8" + target_addr.to_bytes(8, "little") + b"\x48\x85\xC0\x4C\x0F\x45\xC0"
    pm.write_bytes(harvest_fur_address_detour_fn, base_bytes, len(base_bytes))

    # Store fur address
    pm.write_bytes(harvest_fur_address_detour_fn + len(base_bytes),
                   b"\x48\xBB" + int.to_bytes(harvest_fur_address, 8, "little") + b"\x48\x89\x03", 13)

    # Return
    pm.write_bytes(harvest_fur_address_detour_fn + len(base_bytes) + 13, b"\xC3", 1)

    trampoline = b"\x53\x48\xBB" + harvest_fur_address_detour_fn.to_bytes(8, "little") + b"\xFF\xD3\x5B"
    pm.write_bytes(fur_detour_address, trampoline, len(trampoline))
    VirtualProtectEx(pm.process_handle, c_void_p(fur_detour_address), trampoline_size, old_protect.value, c_ulong())
    return harvest_fur_address


def doScreenshot(animalName, animalID):
    window = pygetwindow.getActiveWindow()
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    filename = "screenshots/animals/" + (animalName.strip().upper()) + " " + str(animalID) + ".png"
    screenshot.save(filename)
    logInfo("Screenshot taken: " + filename)


try:
    logInfo("- CotW Harvest Tracker v2.0 -")

    os.makedirs("screenshots/animals", exist_ok=True)

    logInfo("Searching for theHunterCotW_F process...")
    pm = Pymem('theHunterCotW_F.exe')
    logInfo("Base address: " + str(hex(pm.base_address)))

    minTrophyLevelToScreenshot = 0

    while True:
        isScreenshotFeatureEnabled = input("Do you want to enable screenshots of harvests? (y/n): ").strip().lower()
        if isScreenshotFeatureEnabled in ("y", "n"):
            break
        print("Please enter 'y' or 'n'.")

    if isScreenshotFeatureEnabled == "y":
        while True:
            minTrophyLevelToScreenshot = input(
                "What is the minimum trophy rating you want to screenshot? (greatone/diamond/gold/silver/bronze/none): ").strip().lower()
            if minTrophyLevelToScreenshot in ("greatone", "diamond", "gold", "silver", "bronze", "none"):
                minTrophyLevelToScreenshot = getRatingLevelFromText(minTrophyLevelToScreenshot)
                break
            print("Please enter a valid trophy rating name.")
        logInfo("Screenshots will be saved to your screenshots/animals folder in the tracker's folder.")

    logInfo("Searching for harvest data address... Please wait.")
    harvest_base_address = writeHarvestDetour(pm)
    logInfo("Harvest data address: " + str(hex(harvest_base_address)))

    logInfo("Searching for harvest fur address... Please wait.")
    harvest_fur_base_address = writeHarvestFurDetour(pm)
    logInfo("Harvest fur address: " + str(hex(harvest_fur_base_address)))

    lastHarvestWeight = 0

    logInfo("- All is good, we are checking your harvest every second -")
    harvestedAnimalIDs = []

    while True:
        time.sleep(1)

        harvest_address = pm.read_longlong(harvest_base_address)

        if harvest_address == 0:
            continue

        harvest_fur_address = pm.read_longlong(harvest_fur_base_address)

        if harvest_fur_address == 0:
            continue

        try:
            try:
                newHarvestWeight = pm.read_float(harvest_address + 0x24)
            except pymem.exception.MemoryReadError:
                logError("> Failed to read process memory. Have you closed the game? <")
                input("Press Enter to close... ")
                exit(0)

            # Harvest weight has changed.
            if newHarvestWeight != lastHarvestWeight:
                locationName = readLocationNameFromHarvest(harvest_address)

                if locationName is None:
                    continue

                animalName = readAnimalNameFromHarvest(harvest_address)

                if animalName is None:
                    continue

                newAnimal = AnimalData(
                    newHarvestWeight,
                    int.from_bytes(pm.read_bytes(harvest_address + 0x20, 1), "big"),
                    pm.read_int(harvest_address + 0XB0),
                    pm.read_float(harvest_address + 0X3C),
                    pm.read_int(harvest_address + 0X38),
                    pm.read_int(harvest_address + 0X34),
                    int.from_bytes(pm.read_bytes(harvest_address + 0xAC, 1), "big"),
                    pm.read_float(harvest_address + 0X40),
                    datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    pm.read_string(harvest_fur_address, 32)
                )

                newAnimalID = newAnimal.getID()

                if newAnimalID not in harvestedAnimalIDs:
                    harvestedAnimalIDs.append(newAnimalID)
                    logInfo("[" + str(len(harvestedAnimalIDs)) + "] " + animalName + " - " + newAnimal.toString())
                    lastHarvestWeight = newHarvestWeight
                    saveStructure.locations[locationName][animalName].append(newAnimal)
                    saveData(saveStructure)

                    if isScreenshotFeatureEnabled:
                        time.sleep(0.5)
                        # Only record great ones and beyond.
                        if minTrophyLevelToScreenshot >= 5:
                            if newAnimal.ratingIcon >= minTrophyLevelToScreenshot:
                                doScreenshot(animalName, len(saveStructure.locations[locationName][animalName]))
                        else:
                            # Anything else is in ascending order from diamond to none.
                            if newAnimal.ratingIcon <= minTrophyLevelToScreenshot:
                                doScreenshot(animalName, len(saveStructure.locations[locationName][animalName]))

                else:
                    logInfo("Animal has already been harvested: " + newAnimalID)

        except Exception as e:
            print("[EXCEPTION]")
            print(e)
            traceback.print_exc()
        except pymem.exception.MemoryReadError:
            logError("> Failed to read process memory. Have you closed the game? <")
            input("Press Enter to close... ")
            exit(0)

except pymem.exception.ProcessNotFound:
    logError("Failed to attach to theHunterCotW_F process, please start the game before starting this app.")

input("Press Enter to close... ")
