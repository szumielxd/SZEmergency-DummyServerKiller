import subprocess, socket, sys, threading


#
#      CONFIGURATION
#

allowedHosts = ['127.0.0.1', 'localhost']; # list of all hosts allowed to send request
password = "9fhoQv+H95@qP0ydTIC24IC+FqScJqhUxsO*#cM!p#3I!Cvs##Kc!7^&Kg)d8M2*".encode("ascii"); # random password string with exact size of 64 chars
listeningPort = 6066 # port to listen incoming TCP connections


#
#      TCP LISTENER LOOP
#
def onConnect(client: socket, remote):
    try:
        client.settimeout(1);
        if remote[0] in allowedHosts:
            print("Pending connection from /{}:{}".format(remote[0], remote[1]));
            passwd = client.recv(64);
            print(passwd);
            if password == passwd:
                port = int.from_bytes(client.recv(2), 'big');
                print("Request accepted: killing process on port {}...".format(port));
                with subprocess.Popen("fuser -k {}/tcp".format(port), stdout=subprocess.PIPE, shell=True) as proc:
                    if proc.stdout.read():
                        print('Killed!');
                        client.send(b'\x01');
                    else:
                        print('Cannot find process');
                        client.send(b'\x00');
            else:
                print("Request rejected: Wrong password");
                
    except Exception as e:
        print("Something went wrong while listening to /{}:{}: {}".format(remote[0], remote[1], e));
    client.close();


#
#      INITIALIZATION
#
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.bind(('', listeningPort));
    sock.listen(4);
    print("Listening at /{}:{}...".format(sock.getsockname()[0], sock.getsockname()[1]));
    while True:
        threading.Thread(target=onConnect, args=sock.accept()).start();
except:
    if sock != None:
        sock.close();
    print("Caught error: ", sys.exc_info()[0]);
