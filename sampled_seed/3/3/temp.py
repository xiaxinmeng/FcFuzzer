import _testcapi
import time
code = '\nimport threading\nfrom time import sleep\n\ndef func():\n    print("hello from daemon thread")\n    sleep(0.2)\n    print("code run after interpreter death...")\n    sleep(0.1)\n    print("does it crash?")\n    sleep(0.1)\n    print("still alive?")\n    sleep(0.1)\n\nthread = threading.Thread(target=func, daemon=True)\nthread.start()\n# what happens now?\nsleep(0.1)\n'
_testcapi.run_in_subinterp(code)
time.sleep(1)