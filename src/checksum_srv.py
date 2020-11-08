import socket,time,sys
with socket.socket()as main_socket:
 checksum_list=dict();main_socket.bind((sys.argv[1],int(sys.argv[2])));main_socket.listen()
 while new_socket:=main_socket.accept()[0]:
  while new_recv:=new_socket.recv(100):
   split_string=new_recv.split(b"|")
   if split_string[0]==b"BE":checksum_list[split_string[1]]=[time.time()+int(split_string[2]),split_string[3]+b"|"+split_string[4]];new_socket.send(b"OK")
   elif time.time()<checksum_list.get(split_string[1],[0])[0]:new_socket.send(checksum_list[split_string[1]][1])
   else:new_socket.send(b"0|")