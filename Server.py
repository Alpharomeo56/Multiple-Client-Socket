import socket   #To connect two nodes on the network
import select   #Manage multiple socket connections [OS I/O capability]

HEADER_LENGTH = 10  # Constant

IP = "127.0.0.1"
PORT = 1234

#Socket object creation /AF_INET = AddressFamily (IPV4)/Sock_stream = TCP streaming
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO - socket option
# SOL- socket option level
#Reconnecting.
#Option setting the socket to reuse.

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Binding IP and PORT.
server_socket.bind((IP, PORT))

# Making server to  listen to new connections.
server_socket.listen()

# List of sockets
sockets_list = [server_socket]

# Client dictionary key=username,value=data.
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Fucntion to receive message
def receive_message(client_socket):

    try:

        # Receiving header . [ header = len(message) ]
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we dont receive a data.
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8'))

        # Return dictionary
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # Client closing connection [pressing "ctrl+c"]

        return False

while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iteration over notified sockets
    for notified_socket in read_sockets:

        #Accepting new connection
        if notified_socket == server_socket:

            # Accept new connection

            client_socket, client_address = server_socket.accept()

            # Client sending his name
            user = receive_message(client_socket)

            # If client disconnected
            if user is False:
                continue

            # Add accepted socket -> list
            sockets_list.append(client_socket)

            # savig username and user header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # If existing socket sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)

            # IF client disconnected.
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list
                sockets_list.remove(notified_socket)

                # Remove for users list
                del clients[notified_socket]

                continue

            # To know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterating over connected clients
            for client_socket in clients:

                # Only to server
                if client_socket != notified_socket:

                    # Sending username and message

                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

