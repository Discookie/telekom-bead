import socket,random,sys
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
    new_recv=list(new_socket.recv(16))
    print(new_recv)
    if new_recv[:1]==[61]:
     new_recv[0]=b"KY"[new_recv[-1]==guess_number]
     socket_list.remove(new_socket)
     if new_recv[-1]==guess_number:
      for socket_item in socket_list[1:]:socket_item.send(b"V0]=b")
      socket_list[1:]=()
    elif new_recv:new_recv[0]=b"NI"[[new_recv[-1]<guess_number,new_recv[-1]>guess_number][new_recv[0]==60]]
    else:socket_list.remove(new_socket)
    print(new_recv)
    new_socket.send(bytes(new_recv))