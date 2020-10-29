from struct import*
from socket import*
from sys import*
import time
with socket()as main_socket:
 main_socket.connect((argv[1],int(argv[-1])))
 numbers=range(1,101)
 while numbers:
  length=len(numbers)>>1
  main_socket.send(pack("is",numbers[length],{0:b"="}.get(length,b"<")))
  numbers={b"I":numbers[:length],b"N":numbers[length:]}.get(main_socket.recv(1),0)
 main_socket.close()