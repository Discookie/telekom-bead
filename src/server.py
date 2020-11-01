import socket,select,random,sys
with socket.socket()as main_socket:
 main_socket.bind((sys.argv[1],int(sys.argv[2])))
 main_socket.listen()
 socket_list=[main_socket]
 while socket_list:
  readable=select.select(socket_list,socket_list,socket_list)[0]
  for new_socket in readable:
   if socket_list[0]==new_socket:
    if socket_list[:1]==socket_list:guess_number=random.randint(1,100)
    socket_list+=[new_socket.accept()[0]]
   else:
    new_recv=list(new_socket.recv(5))
    if new_recv[0]==61:
     socket_list.remove(new_socket)
     new_recv[0]=b"KY"[new_recv[1]==guess_number]
     if new_recv[1]==guess_number:
      for socket_item in socket_list[1:]:socket_item.send(b"V0]=b")
      socket_list[1:]=()
    elif new_recv:new_recv[0]=b"NI"[[new_recv[1]>guess_number,new_recv[1]<guess_number][new_recv[0]==61]]
    else:socket_list.remove(new_socket)
    new_socket.send(bytes(new_recv))