import socket,hashlib,sys
with socket.socket()as main_socket:
 md5_processor=hashlib.md5();main_socket.bind((sys.argv[1],int(sys.argv[2])));main_socket.listen();cli_socket=main_socket.accept()[0]
 with open(sys.argv[-1],"wb")as out_file:
  while out_file.write(new_recv:=cli_socket.recv(1000)):md5_processor.update(new_recv)
with socket.socket()as checksum_socket:
 checksum_socket.connect((sys.argv[3],int(sys.argv[-3])));checksum_socket.send(b"KI|"+sys.argv[-2].encode())
 if checksum_socket.recv(1000)[3:]==md5_processor.hexdigest().encode():print("CSUM OK")
 else:print("CSUM CORRUPTED")
 checksum_socket.close()