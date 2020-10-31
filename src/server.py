from struct import*
from socket import*
from random import*
from select import*
from sys import*
with socket()as main_socket:
 main_socket.bind((argv[1],int(argv[-1])));main_socket.listen();socket_list=[main_socket]
 while socket_list:
  readable=select(socket_list,socket_list,socket_list)[0]
  for new_socket in readable:
   if socket_list[0]==new_socket:socket_list+=new_socket.accept()[:1];guess_number=guess_number if socket_list[2:]else randint(1,100);continue
   new_recv=bytearray(new_socket.recv(5))
   if new_recv[:1]==b"=":
    if new_recv[1]-guess_number:new_recv[:1]=b"K";new_socket.send(new_recv);socket_list.remove(new_socket);continue
    for socket_item in socket_list[1:]:new_recv[0]=b"VY"[socket_item==new_socket];socket_item.send(new_recv);socket_list.remove(socket_item)
   elif new_recv:new_recv[0]=b"NI"[(new_recv[:1]==b"<")==(guess_number<new_recv[1])];new_socket.send(new_recv)
   else:socket_list.remove(new_socket)