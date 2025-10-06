import ctypes
from ctypes import wintypes

MEM_COMMIT      = 0x00001000
MEM_RESERVE     = 0x00002000
MEM_RELEASE     = 0x00008000

PAGE_READONLY          = 0x02
PAGE_READWRITE         = 0x04
PAGE_EXECUTE           = 0x10
PAGE_EXECUTE_READ      = 0x20
PAGE_EXECUTE_READWRITE = 0x40

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

VirtualAlloc          = kernel32.VirtualAlloc
VirtualAlloc.restype  = ctypes.c_void_p
VirtualAlloc.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]

VirtualFree          = kernel32.VirtualFree
VirtualFree.restype  = wintypes.BOOL
VirtualFree.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD]

VirtualProtect          = kernel32.VirtualProtect
VirtualProtect.restype  = wintypes.BOOL
VirtualProtect.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.PDWORD]

GetLastError          = kernel32.GetLastError
GetLastError.restype  = wintypes.DWORD
GetLastError.argtypes = []

class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
        ('wProcessorArchitecture', wintypes.WORD),
        ('wReserved', wintypes.WORD),
        ('dwPageSize', wintypes.DWORD),
        ('lpMinimumApplicationAddress', wintypes.LPVOID),
        ('lpMaximumApplicationAddress', wintypes.LPVOID),
        ('dwActiveProcessorMask', wintypes.DWORD),
        ('dwNumberOfProcessors', wintypes.DWORD),
        ('dwProcessorType', wintypes.DWORD),
        ('dwAllocationGranularity', wintypes.DWORD),
        ('wProcessorLevel', wintypes.WORD),
        ('wProcessorRevision', wintypes.WORD)
    ]

GetSystemInfo          = kernel32.GetSystemInfo
GetSystemInfo.restype  = None
GetSystemInfo.argtypes = [ctypes.c_void_p]





# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=




# fetch the size of a page from windows
systemInfoStruct = SYSTEM_INFO()
GetSystemInfo(ctypes.pointer(systemInfoStruct))
pageSize = systemInfoStruct.dwPageSize
del systemInfoStruct

# information about a page that has been allocated
class AllocatedPageInformation:
    def __init__(self, start = 0, end = 0):
        self.start = 0
        self.end = 0

        # a bool for each 64 byte chunk of the file being used
        # first 64 bytes are for internal tracking
        self.inUse = []

AllAllocatedPageStarts = []
AllAllocatedPageFields = []
AllocatedPageMetadata  = []

# get a memory page from windows
def AllocatePage() -> ctypes.c_void_p:
    pageStart = VirtualAlloc(0, pageSize, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)

    if pageStart != None:
        AllocatedPageMetadata.append(AllocatedPageInformation(pageStart, pageSize))
        AllAllocatedPageStarts.append(pageStart)
        AllAllocatedPageFields.append(ctypes.c_uint8.from_address(pageStart))

    return pageStart

# return a memory page to windows
def DeallocatePage(pageStart) -> bool:
    index = -1

    for i in range(len(AllAllocatedPageStarts)):
        if AllAllocatedPageStarts[i] == pageStart:
            index = i
            break

    if index == -1:
        return False

    if VirtualFree(AllAllocatedPageStarts[i], 0, MEM_RELEASE):
        del AllAllocatedPageFields[index]
        del AllAllocatedPageStarts[index]
        del AllocatedPageMetadata[index]

        return True

    return False
