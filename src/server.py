from struct import*
from socket import*
from random import*
from select import*
from sys import*
with socket()as main_socket:
 main_socket.bind((argv[1],int(argv[-1])))
 main_socket.listen()
 socket_list=[main_socket]
 while[1]:
  readable=select(socket_list,[],[])[0]
  for new_socket in readable:
   if socket_list[0] is new_socket:
    socket_list+=new_socket.accept()[:1];guess_number=guess_number if socket_list[2:]else randint(1,100)
   else:
    new_recv = new_socket.recv(5)
    if new_recv:
     received_num,received_char=unpack("is",new_recv)
     if b"="==received_char:
      if guess_number-received_num:new_socket.send(b"K");socket_list.remove(new_socket)
      else:
       for socket_item in socket_list[1:]:socket_item.send(b"Y"if socket_item==new_socket else b"V");socket_list.remove(socket_item)
     else:new_socket.send(b"N"if("<"==received_char)==(guess_number<received_num)else b"I")
    else:socket_list.remove(new_socket)