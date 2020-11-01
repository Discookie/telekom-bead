from socket import*;from sys import*
with socket()as main_socket:
 main_socket.connect((argv[1],int(argv[-1])));numbers=range(1,101)
 while numbers:length=len(numbers)>>1;main_socket.send(bytes([61-(length>0),numbers[length]]+[0]*3));numbers={b"I":numbers[:length],b"N":numbers[length:]}.get(main_socket.recv(5)[:1],0)
 main_socket.close()