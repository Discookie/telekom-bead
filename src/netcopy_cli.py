import socket,hashlib,sys
with socket.socket()as cli_socket:
 in_file,md5_processor=open(sys.argv[-1],"rb"),hashlib.md5();cli_socket.connect((sys.argv[1],int(sys.argv[2])))
 while new_recv:=in_file.read(1000):cli_socket.send(new_recv);md5_processor.update(new_recv)
 with socket.socket()as checksum_socket:checksum_socket.connect((sys.argv[3],int(sys.argv[-3])));checksum_socket.send(b"|".join((b"BE",sys.argv[-2].encode(),b"5|32",md5_processor.hexdigest().encode())));checksum_socket.recv(3);checksum_socket.close()
 cli_socket.close()