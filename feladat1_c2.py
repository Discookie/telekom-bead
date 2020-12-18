from json import*
from datetime import*
from subprocess import*
with open(sys.argv[1])as t:
 e=t.readlines()
 with open("traceroute.json","w")as t:dump({"traces":[{"target":c.split(",")[1][:-1],"output":check_output(["traceroute",c.split(",")[1][:-1]]).decode()}for c in e[:10]+e[-10:]],"system":"linux","date":date.today().strftime("%Y%m%d")},t)
 with open("ping.json","w")as t:dump({"pings":[{"target":c.split(",")[1][:-1],"output":check_output(["ping","-c10","-i,2",c.split(",")[1][:-1]]).decode()}for c in e[:10]+e[-10:]],"system":"linux","date":date.today().strftime("%Y%m%d")},t)
