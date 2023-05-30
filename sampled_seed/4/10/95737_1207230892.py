import time
import ctypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

CTRL_C_EVENT = 0

# Enable CTRL_C_EVENT for the current process.
kernel32.SetConsoleCtrlHandler(None, False)

@ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_ulong)
def handler(event):
    print('event:', event)
    if event != CTRL_C_EVENT:
        return False 
    return True

kernel32.SetConsoleCtrlHandler(handler, True)

print('Type Ctrl-Break to exit.')
while True:
    time.sleep(1)