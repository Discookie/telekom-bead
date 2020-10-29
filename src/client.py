from struct import*
from socket import*
from sys import*
import time
with socket()as main_socket:
 main_socket.connect((argv[1],int(argv[-1])))
 numbers=range(1,101)
 while numbers:
  length=len(numbers)>>1
  print(numbers[length])
  main_socket.send(pack("is",numbers[length],{0:b"="}.get(length,b"<")))
  time.sleep(1)
  x=main_socket.recv(1);print(x)
  numbers={b"I":numbers[:length],b"N":numbers[length:]}.get(x,0)
  print(numbers)
 main_socket.close()