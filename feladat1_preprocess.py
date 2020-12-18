import gzip
import zlib
import base64

code = '''
from json import*
from datetime import*
from subprocess import*
with open(sys.argv[1])as i:
 e=i.readlines()
 with open("traceroute.json","w")as i:dump({"traces":[{"target":c.split(",")[1][:-1],"output":check_output(["traceroute",c.split(",")[1][:-1]]).decode()}for c in e[:10]+e[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},i)
 with open("ping.json","w")as i:dump({"pings":[{"target":c.split(",")[1][:-1],"output":check_output(["ping","-c10","-i,2",c.split(",")[1][:-1]]).decode()}for c in e[:10]+e[-10:]],"system":"linux","date":f'{date.today():%Y%m%d}'},i)
'''[1:-1]


compressed_code = base64.b85encode(zlib.compress(str.encode(code), 9))

print(len(code))
print(len(compressed_code))
print(compressed_code)

decompressed_code = zlib.decompress(base64.b85decode(compressed_code))

print(decompressed_code)

exec(decompressed_code)