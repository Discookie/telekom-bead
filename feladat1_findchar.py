import gzip
import zlib
import base64
from lzma import*

code = '''
from json import*
from datetime import*
from subprocess import*
with open(sys.argv[1])as #i:
 #j=#i.readlines()
 with open("traceroute.json","w")as #k:dump({"traces":[{"target":#l.split(",")[1][:-1],"output":check_output(["traceroute",#l.split(",")[1][:-1]]).decode()}for #l in #j[:10]+#j[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},#k)
 with open("ping.json","w")as #k:dump({"pings":[{"target":#l.split(",")[1][:-1],"output":check_output(["ping","-c10",#l.split(",")[1][:-1]]).decode()}for #l in #j[:10]+#j[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},#k)
'''[1:-1]

results = {}

best_result = 99999
best_combinations = []

for i in map(chr,range(97,123)):
    results[i] = {}
    for j in map(chr,range(97,123)):
        if i == j: continue
        results[i][j] = {}
        for k in map(chr,range(97,123)):
            if j == k: continue
            results[i][j][k] = {}
            for l in map(chr,range(97,123)):
                new_code = code.replace("#i", i).replace("#j", j).replace("#k",k).replace("#l",l)
                result = len(base64.b85encode(zlib.compress(str.encode(new_code), 9)))
                
                results[i][j][k][l] = result
                if (result == best_result):
                    best_combinations += [(i, j, k, l)]
                elif result < best_result:
                    best_result = result
                    best_combinations = [(i, j, k, l)]

print("Best result:", best_result, "with combinations", best_combinations)

