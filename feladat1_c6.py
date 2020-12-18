from json import*
from datetime import*
from subprocess import*
with open(sys.argv[1])as i:
 e=i.readlines()
 with open("traceroute.json","w")as i:dump({"traces":[{"target":f.split(",")[1][:-1],"output":f'{check_output(["traceroute",f.split(",")[1][:-1]])}'}for f in e[:10]+e[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},i)
 with open("ping.json","w")as i:dump({"pings":[{"target":f.split(",")[1][:-1],"output":f'{check_output(["ping","-c10","-i,2",f.split(",")[1][:-1]])}'}for f in e[:10]+e[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},i)
