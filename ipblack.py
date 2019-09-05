import threading
import time
import subprocess
import select

def check(flag):
    for ip in flag:
        if int(time.time()) - flag[ip][-1] > 600:
            del flag[ip]
        elif int(time.time()) - flag[ip][0] > 300 and len(flag[ip]) > 100:
            f = open('ip.black','a')
            f.write("deny " + ip + ";" + "\n")
            f.close

def logs():

        f = subprocess.Popen(['tail','-F','access.log'],\
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)
        flag = {}
#        count = 0
        last_check_ts = time.time()
        while True:
            while p.poll(1):
                time_list = []
                line = f.stdout.readline()
                j = line.split(' ')[0]
                i = int(time.time())
                if j in flag:
                    flag[j].append(i)
                else:
                    time_list.append(i)
                    flag[j] = time_list
#                count = count + 1
#                print len(flag)
            if time.time() - last_check_ts > 60:
                check(flag)
                last_check_ts = time.time()
            time.sleep(1)

logs()

"""
600秒内无访问的ip从字典中删除；
300秒内访问超过100次的ip加入黑名单；
"""
