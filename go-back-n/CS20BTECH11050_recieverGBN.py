import socket
import select

recieverIP = "10.0.0.2"
recieverPort   = 20002
senderAddressPort = ("10.0.0.1", 20001)
bufferSize  = 1024 #Message Buffer Size

# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )

curr_seq_no = 0

while True:
#wait to recieve message from the server
    bdata, baddr = socket_udp.recvfrom(bufferSize)
    if(bdata):
        print("File Name:",bdata.decode())
        fname = "recieved.jpg"
        f = open(fname,'wb')

    while True:
        ready = select.select([socket_udp], [], [], 5)

        if ready[0]:
            data, addr = socket_udp.recvfrom(bufferSize)
            seq_no = int.from_bytes(data[:2],"big")
            print("Recv pkt:",seq_no)
            end_byte = data[2:3]
            # print(int(end_byte))
            rdata = data[3:]

            if(seq_no==curr_seq_no):
                ack = ("ACK "+str(seq_no)).encode()
                socket_udp.sendto(ack,addr)
                f.write(rdata)
                curr_seq_no+=1
            else:
                ack = ("ACK "+str(curr_seq_no-1)).encode()
                socket_udp.sendto(ack,addr)



        else:
            print ("%s has been transfered successfully!" % fname)
            f.close()
            break

    if(f.closed):
        socket_udp.close()
        break
