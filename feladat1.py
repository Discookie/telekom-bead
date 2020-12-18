import sys
import json
import datetime
import subprocess

with open(sys.argv[1]) as read:
    readlines = read.readlines()
    readlines = readlines[:1] + readlines[-1:]

    readli = [{"target": read.split(",")[1][:-1], "output": subprocess.check_output(["traceroute", read.split(",")[1][:-1]]).decode("utf-8")} for read in readlines]
    with open("traceroute.json", "w") as readl:
        json.dump({"date": datetime.date.today().strftime("%Y%m%d"), "system": "linux", "traces": readli}, readl)

    readli = [{"target": read.split(",")[1][:-1], "output": subprocess.check_output(["ping", "-c10", "-i,2", read.split(",")[1][:-1]]).decode("utf-8")} for read in readlines]
    with open("pings.json", "w") as readl:
        json.dump({"date": datetime.date.today().strftime("%Y%m%d"), "system": "linux", "pings": readli}, readl)
