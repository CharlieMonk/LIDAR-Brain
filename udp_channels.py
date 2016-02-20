import socket
#
#  Create the infra for two-way communication channel using UDP
#  Set receive from timeout to .001 seconds to avoid blocking for
#  long.
#
class UDPChannel:
        # Useful defaults permit minimal arguments for simple test.
        # On one end:
        #      sender = UDPChannel()
        #    receiver = UDPChannel(local_port=sender.remote_port, remote_port=sender.local_port)
        def __init__(self, local_ip="127.0.0.1", local_port=52777,
                     remote_ip="127.0.0.1", remote_port=52888,
                     timeout_in_seconds=0.001, receive_buffer_size=1024):
                """Create the sending and receiving sockets for a communcation channel"""
                self.local_ip = local_ip
                self.local_port = local_port
                self.remote_ip = remote_ip
                self.remote_port = remote_port

                # create the receive socket
                self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.receive_socket.bind((local_ip, local_port))

                # and the sending socket
                self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                # cache other configurable parameters
                self.timeout_in_seconds = timeout_in_seconds
                self.receive_buffer_size = receive_buffer_size

        def send_to(self, message):
                self.send_socket.sendto(message, (self.remote_ip, self.remote_port))
        def reply_to(self, message, (ip, port)):
                self.send_socket.sendto(message, (ip, port))

        def receive_reply(self):
                self.send_socket.settimeout(self.timeout_in_seconds)
                return self.send_socket.recvfrom(self.receive_buffer_size)

        def receive_from(self):
                self.receive_socket.settimeout(self.timeout_in_seconds)
                return self.receive_socket.recvfrom(self.receive_buffer_size)

