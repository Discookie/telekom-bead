import sys,socket
with socket.socket()as main_socket:
 main_socket.connect((sys.argv[1],int(sys.argv[-1])));numbers=range(1,101)
 while numbers:print((61-(len(numbers)>1),numbers[len(numbers)>>1],0,0,0));main_socket.send(bytes((61-(len(numbers)>1),numbers[len(numbers)>>1],0,0,0)));numbers={b"N":numbers[len(numbers)>>1:],b"I":numbers[:len(numbers)>>1]}.get((x:=main_socket.recv(5),print(x),x[:1])[2],0)
 main_socket.close()