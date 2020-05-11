import socket
import errno #This module makes available standard errno system symbols.
import sys #This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# Creating a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If message is not empty - send it
    if message:

        # Encoding message to bytes, preparing header and converting to bytes and then sending.
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # loop over received messages and printing them
        while True:

            # Receive our "header" containing username length, its constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # Closing connection
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Converting header to int value
            username_length = int(username_header.decode('utf-8'))

            # Receiving username and decoding it
            username = client_socket.recv(username_length).decode('utf-8')

            # Now doing same for the message (decoding)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} > {message}')

    except IOError as e:
        # When there is no incoming data error is going to be raised

        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK: #Try again and block
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # When we recieve nothing
        continue

    except Exception as e:
        # Any other exception- exit.
        print('Reading error: '.format(str(e)))
        sys.exit()