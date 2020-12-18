from json import*
from datetime import*
from subprocess import*
with open(sys.argv[1])as i:
 e=i.readlines()
 with open("traceroute.json","w")as i:dump({"traces":[{"target":c.split(",")[1][:-1],"output":check_output(["traceroute",c.split(",")[1][:-1]]).decode()}for c in e[:10]+e[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},i)
 with open("ping.json","w")as i:dump({"pings":[{"target":c.split(",")[1][:-1],"output":check_output(["ping","-c10",c.split(",")[1][:-1]]).decode()}for c in e[:10]+e[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},i)
