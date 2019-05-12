import socket, sys, threading
import msg

class Client(threading.Thread):
    """Supports concurrent clients with multi-threading

    outgoing stream: using socket
    incoming stream: using file-like object (buffered)
                     assuming response messages are separated by new line
    """
    def __init__(self, server_addr):
        threading.Thread.__init__(self)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_addr)
        # convert socket to file-like obj only for imcoming messages
        self.in_file = self.sock.makefile('rb')
        self.sent_bytes = []
        self.recv_bytes = []

    def run(self):
        print('%s started' % self.getName())
        for message in msg.msgs(20, length=2000):
            n_sent = self.sock.send(message)
            self.sent_bytes.append(n_sent)
            data = self.in_file.readline()      # receive response
            if not data:
                print('Server closing')
                break
            self.recv_bytes.append(len(data))
        self.sock.close()                       # to send eof to server

if __name__ == '__main__':
    # serv_addr = ('np.hufs.ac.kr', 7)
    serv_addr = ('localhost', 10007)
    n_clients = 3
    if len(sys.argv) == 2:
        n_clients = int(sys.argv[1])

    # create and start n client thread objects
    threads = []
    for i in range(n_clients):
        cli = Client(serv_addr)
        cli.start()
        threads.append(cli)

    # Wait for terminating child threads
    for t in threads:
        t.join()        # wait for terminating child thread t
        print(t)
        msg.report(t.sent_bytes, t.recv_bytes)
