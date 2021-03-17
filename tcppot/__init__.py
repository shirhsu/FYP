import logging
import threading
from socket import socket, timeout

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class HoneyPot(object):

    def __init__(self, bind_ip, ports, log_filepath):
        if len(ports) < 1:
            raise Exception("There are no ports provided.")
        for port in ports:
            print("Listening on port: %s" % port)

        self.bind_ip = bind_ip
        self.ports = ports
        self.log_filepath = log_filepath
        self.listener_threads = {}
        self.logger = self.prepare_logger()

        self.logger.info("Initializing Honeypot!......")
        self.logger.info("Ports: %s" % self.ports)
        self.logger.info("Logfile_path: %s" % self.log_filepath)

    def handle_connection(self, client_socket, port, ip, remote_port):
        self.logger.info("Data received on port: %s: From %s:%d:" % (port, ip, remote_port))
        client_socket.settimeout(3)
        try:
            data = client_socket.recv(64)
            self.logger.info("Data received on port: %s: From %s:%d: %s" % (port, ip, remote_port, data))
            client_socket.send("Access Denied!....\n".encode('utf8'))
        except timeout:
            pass
        client_socket.close()

    def start_new_listener_thread(self, port, ):
        listener = socket()
        listener.bind((self.bind_ip, int(port)))
        listener.listen(5)
        while True:
            client, addr = listener.accept()
            # print("Accepted connection from %s:%d" % (addr[0], addr[1]))
            client_handler = threading.Thread(target=self.handle_connection, args=(client, port, addr[0], addr[1]))
            client_handler.start()

    def star_listening(self):
        for port in self.ports:
            self.listener_threads[port] = threading.Thread(target=self.start_new_listener_thread, args=(port,))
            self.listener_threads[port].start()

    def run(self):
        self.star_listening()
        # while True:
        # pass

    def prepare_logger(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=self.log_filepath,
                            filemode='w')
        logger = logging.getLogger(__name__)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        return logger
