from json import*
from datetime import*
from subprocess import*
with open(sys.argv[1])as i:
 t=i.readlines()
 with open("traceroute.json","w")as i:dump({"traces":[*map(lambda f:{"target":f.split(",")[1][:-1],"output":f'{check_output(["traceroute",f.split(",")[1][:-1]])}'},t[:10]+t[-10:])],"system":"linux","date":date.today().strftime("%Y%m%d")},i)
 with open("ping.json","w")as i:dump({"pings":[*map(lambda f:{"target":f.split(",")[1][:-1],"output":f'{check_output(["ping","-c10","-i,2",f.split(",")[1][:-1]])}'},t[:10]+t[-10:])],"system":"linux","date":date.today().strftime("%Y%m%d")},i)
