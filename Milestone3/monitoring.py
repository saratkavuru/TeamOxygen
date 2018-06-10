import requests
import time

def main():
    f = open('inventory','r')
    found = False
    ips = []
    for line in f.readlines():
        if line:
            if "iTrust" in line:
                found = True
                continue
            if found and 'ansible' in line:
                ip = line.split()[0]
                ips.append(ip)
    i=0
    while i<120:
        a = []
        for ip in ips:
            try:
                r = requests.get('http://{}:8080/iTrust2/login'.format(ip))
                a+= [ip + " : RUNNING"]
            except Exception as e:
                a+= [ip + " : DOWN"]
        print("----- HEARTBEAT STATUS -----")
        print(a)
        time.sleep(5)
        i+=1

main()