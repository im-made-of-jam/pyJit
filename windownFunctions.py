import ctypes
from ctypes import wintypes

MEM_COMMIT      = 0x00001000
MEM_RESERVE     = 0x00002000

PAGE_READONLY   = 0x02
PAGE_READWRITE  = 0x04
PAGE_EXECUTE    = 0x10

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

VirtualAlloc          = kernel32.VirtualAlloc
VirtualAlloc.restype  = ctypes.c_void_p
VirtualAlloc.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]

VirtualFree          = kernel32.VirtualFree
VirtualFree.restype  = wintypes.BOOL
VirtualFree.argtypes = [wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD]

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





systemInfoStruct = SYSTEM_INFO()
GetSystemInfo(ctypes.pointer(systemInfoStruct))
pageSize = systemInfoStruct.dwPageSize
del systemInfoStruct

class AllocatedPageInformation:
	def __init__(self, start = 0, end = 0):
		self.start = 0
		self.end = 0
		self.inUse = [] # a bool for each 1024 byte chunk of the file being used

AllAllocatedPageStarts = []
AllocatedPageInformation = []

def AllocatePage():
	pageStart = VirtualAlloc(0, pageSize, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
	return pageStart

def DeallocatePage():
	...
