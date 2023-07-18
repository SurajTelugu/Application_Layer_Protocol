import socket
import time

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1021 #Message Buffer Size
time_out = float(input("Enter timeout in millisec:"))/1000

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.sendto("testFile.jpg".encode(), recieverAddressPort)
print("Sending Image ...")

f=open("testFile.jpg","rb")
data = f.read(bufferSize)
seq_no = 0


# float(input("Enter time out (in millisec):"))*1000
no_of_packet = 0
time_out_cnt = 0
start_time = time.time()
while(data):
    b = 0
    data = seq_no.to_bytes(2,'big') + str(b).encode() +  data
    socket_udp.sendto(data , recieverAddressPort)
    no_of_packet+=1

    while True:

        try:
            socket_udp.settimeout(time_out)
            recv_ack = socket_udp.recvfrom(1024)
            ack_msg, ack_seq_no = recv_ack[0].decode().split()
            print("Recv ack:",ack_msg,ack_seq_no)
            if(int(ack_seq_no) == seq_no):
                if(seq_no==0): seq_no = 1
                else: seq_no = 0
                break
        
        except socket.timeout as e:
            print(e)
            time_out_cnt+=1
            socket_udp.sendto(data , recieverAddressPort)
            exp_time = time.time() + time_out


    data = f.read(bufferSize)

end_time = time.time()

Ack_time = end_time - start_time
print(Ack_time)
print(no_of_packet)
print(no_of_packet/Ack_time)
print(time_out_cnt)

socket_udp.close()
f.close()