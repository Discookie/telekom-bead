import socket,hashlib,sys
with socket.socket()as main_socket:
 out_file,md5_processor=open(sys.argv[5],"wb"),hashlib.md5();main_socket.bind((sys.argv[1],int(sys.argv[2])));main_socket.listen();cli_socket=main_socket.accept()[0]
 while out_file.write(new_recv:=cli_socket.recv(1000)):md5_processor.update(new_recv)
with socket.socket()as checksum_socket:checksum_socket.connect((sys.argv[3],int(sys.argv[-3])));checksum_socket.send(b"KI|"+sys.argv[-2].encode());print("CSUM","OK"if md5_processor.hexdigest().encode()==checksum_socket.recv(1000)[3:]else"CORRUPTED");checksum_socket.close()