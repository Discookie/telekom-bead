from socket import*;from random import*;from select import*;from sys import*
with socket()as main_socket:
 main_socket.bind((argv[1],int(argv[-1])));main_socket.listen();socket_list=[main_socket]
 while socket_list:
  readable=select(socket_list,socket_list,socket_list)[0]
  for new_socket in readable:
   if socket_list[0]==new_socket:
    if socket_list[:1]==socket_list:guess_number=randint(1,100)
    socket_list+=new_socket.accept()[:1];continue
   new_recv=bytearray(new_socket.recv(5))
   if new_recv[:1]==b"=":
    socket_list.remove(new_socket);new_recv[0]=b"KY"[new_recv[1]==guess_number]
    if new_recv[1]==guess_number:
     for socket_item in socket_list[1:]:socket_item.send(b"V]==b");socket_list.remove(socket_item)
   elif new_recv:new_recv[0]=b"NI"[(new_recv[:1]==b"<")==(guess_number<new_recv[1])]
   else:socket_list.remove(new_socket)
   new_socket.send(new_recv)