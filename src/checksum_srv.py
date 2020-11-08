import socket,select,time,sys
with socket.socket()as main_socket:
 main_socket.bind((sys.argv[1],int(sys.argv[2])))
 main_socket.listen()
 checksum_list,socket_list={},[main_socket]
 while socket_list:
  readable=select.select(socket_list,socket_list,socket_list)[0]
  for new_socket in readable:
   if socket_list[0]==new_socket:socket_list+=[new_socket.accept()[0]]
   elif new_recv:=new_socket.recv(100):
    split_string=new_recv.split(b"|")
    if split_string[0]==b"BE":checksum_list[split_string[1]]=[time.time()+int(split_string[2]),split_string[3]+b"|"+split_string[4]];new_socket.send(b"OK")
    elif time.time()<checksum_list.get(split_string[1],[0])[0]:new_socket.send(checksum_list[split_string[1]][1])
    else:new_socket.send(b"0|")
   else:socket_list.remove(new_socket)