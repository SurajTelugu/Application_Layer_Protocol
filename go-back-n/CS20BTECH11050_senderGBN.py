import socket
import time

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1021 #Message Buffer Size
Window_Size_N = int(input("Enter Window Size:"))
time_out = 0.03

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.sendto("testFile.jpg".encode(), recieverAddressPort)
print("Sending Image ...")

f=open("testFile.jpg","rb")
packets = []
it = 0
data = f.read(bufferSize)
while data:
    packets.append(data)
    it+=1
    data = f.read(bufferSize)


no_of_packets = len(packets)
base_pack = 0
curr_pack = 0
fbyte = 0

no_timeout = 0

start = time.time()
while(base_pack < no_of_packets):

    while(curr_pack < base_pack + Window_Size_N and curr_pack < no_of_packets):
        pack = curr_pack.to_bytes(2,'big') + str(0).encode() + packets[curr_pack]
        socket_udp.sendto(pack, recieverAddressPort)
        curr_pack+=1
    
    try:
        socket_udp.settimeout(time_out)
        while True:
            recv_ack = socket_udp.recvfrom(1024)
            ack_msg, ack_seq_no = recv_ack[0].decode().split()
            print("Recv ack:",ack_msg,ack_seq_no)
            ackno = int(ack_seq_no)
            if(base_pack <= ackno): 
                base_pack = ackno + 1
                break

    except socket.timeout as e:
        print(e)
        no_timeout+=1
        curr_pack = base_pack

end = time.time()
tottime = end - start
print(no_of_packets/tottime)
print(no_timeout)

socket_udp.close()
f.close()