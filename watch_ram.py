import os
import time

maxkb = 0
emp = 0
c = 0
try: 
    while True:
        r = os.popen("ps aux | grep 'aqppp2' | grep -v grep")
        res = r.read()
        r.close()
        # print(res)
        if emp > 5000:
            break
        if len(res) == 0:
            if c != 0:
                emp += 1
            time.sleep(0.01)
            continue
        pid = res.split()[1]
        r = os.popen(f"cat /proc/{pid}/status | grep -e VmRSS")
        ram_str = r.read()
        print(ram_str)
        if "cat" in ram_str:
            continue
        try:
            ram = int(ram_str.split()[1])
        except:
            continue
        print(pid)
        #print(ram)
        maxkb = max(ram, maxkb)
        with open("max_ram_train.txt","w") as f:
            f.write(str(maxkb))
        time.sleep(0.01)
        c += 1
except KeyboardInterrupt:
    maxkb = max(ram, maxkb)
    with open("max_ram_train_group.txt","w") as f:
        f.write(str(maxkb))