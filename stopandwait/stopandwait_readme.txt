$ cd /home/p4/<folder>

$ sudo mn
$ xterm h1 h2

In h2: (Server Running)

$ sudo tc qdisc add dev h1-eth0 root netem rate 10Mbit limit 100 delay 5ms loss 5% (For Network conditions)
$ python3 <receivername>.py

In h1: (Client Running)

$ sudo tc qdisc add dev h1-eth0 root netem rate 10Mbit limit 100 delay 5ms loss 5%   (For Network conditions)
$ python3 <servername>.py

Enter the timeout in milliseconds as input to see the results