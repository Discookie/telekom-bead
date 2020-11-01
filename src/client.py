import sys,socket
with socket.socket()as main_socket:
 main_socket.connect((sys.argv[1],int(sys.argv[2])));numbers=range(1,101)
 while numbers:length=len(numbers)>>1;main_socket.send(bytes([61-(length>0),numbers[length],0,0,0]));numbers={1:numbers[:length],6:numbers[length:]}.get(main_socket.recv(5)[0]-72,0)
 main_socket.close()