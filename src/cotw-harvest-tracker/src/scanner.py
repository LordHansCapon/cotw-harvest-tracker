from pymem.ressources.structure import MEMORY_BASIC_INFORMATION
from pymem.ressources.kernel32 import VirtualQueryEx
from ctypes import sizeof, byref


def scan_process(pm, pattern):
    handle = pm.process_handle
    address = 0
    matches = []

    mbi = MEMORY_BASIC_INFORMATION()

    while VirtualQueryEx(handle, address, byref(mbi), sizeof(mbi)):
        committed = mbi.State == 0x1000
        readable = mbi.Protect in (0x02, 0x04, 0x20, 0x40)

        if committed and readable:
            base = mbi.BaseAddress
            size = mbi.RegionSize

            try:
                buf = pm.read_bytes(base, size)
            except Exception:
                address += mbi.RegionSize
                continue

            idx = buf.find(pattern)
            while idx != -1:
                matches.append(base + idx)
                idx = buf.find(pattern, idx + 1)

        address += mbi.RegionSize

    return matches
