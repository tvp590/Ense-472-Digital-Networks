import socket
import threading

PORT = 8000
PC_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(PC_NAME)
TCP_ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!Q"
HEADER_SIZE_IN_BYTES = 8

def send(sock, message):
    message_encoded = message.encode(FORMAT) 
    message_length = len(message_encoded)
    message_send_length = str(message_length).encode(FORMAT)
    padding_needed = HEADER_SIZE_IN_BYTES - len(message_send_length)
    # this repeats the space byte by padding needed times
    padding = b' ' * padding_needed
    padded_message_send_length = message_send_length + padding
    sock.send(padded_message_send_length)
    sock.send(message_encoded)

def receive(sock,addr):
    while True:
        try:
            message_length = sock.recv(HEADER_SIZE_IN_BYTES).decode(FORMAT).strip()
            if message_length:
                message_length = int(message_length)
                message = sock.recv(message_length).decode(FORMAT)
                print (f"{message}")
        except:
            break

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(TCP_ADDR)

    # Get client's address and port
    client_address = client.getsockname()
    
    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive, args=(client,client_address))
    receive_thread.daemon = True
    receive_thread.start()

    try:
        message = input(f"enter message, or enter '{DISCONNECT_MESSAGE}' to diconnect: ")
        while message != DISCONNECT_MESSAGE:
            send(client, message)
            message = input()
    except KeyboardInterrupt:
        pass

    send(client, DISCONNECT_MESSAGE)
    client.close()
