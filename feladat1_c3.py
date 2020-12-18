from json import*
from datetime import*
from subprocess import*
with open(sys.argv[1])as e:
 e=e.readlines()
 e=e[:10]+e[-10:]
 re=[{"target":e[e.find(",")+1:-1],"output":check_output(["traceroute",e[1+e.find(","):-1]])} for e in e]
 with open("traceroute.json","w")as e:dump({"traces":re,"system":"linux","date":date.today().strftime("%Y%m%d")},e)
 re=[{"target":e[e.find(",")+1:-1],"output":check_output(["ping","-c10","-i,2",e[1+e.find(","):-1]])} for e in e]
 with open("pings.json","w")as e:dump({"pings":re,"system":"linux","date":date.today().strftime("%Y%m%d")},e)
