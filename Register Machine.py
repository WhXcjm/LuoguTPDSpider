import time
key = int(time.strftime("%Y%m%d"))** 11 * int(time.strftime("%m%Y%d")) % 1000001
print(key)
input()