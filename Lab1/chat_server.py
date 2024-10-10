import socket
import threading

PORT = 8000
PC_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(PC_NAME)
TCP_ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!Q"
HEADER_SIZE_IN_BYTES = 8
client_sockets = {}  # key: socket, value: username
lock = threading.Lock()


# one instance of this will run for each client in a thread
def handle_client(conn, addr, server_active):
    print (f"[NEW CONNECTION] {addr} connected.")
    
    try: 
        send(conn, "Please choose a username: ")
        username_length_encoded = conn.recv(HEADER_SIZE_IN_BYTES)
        username_length = int(username_length_encoded.decode(FORMAT).strip())
        username = conn.recv(username_length).decode(FORMAT)

        client_sockets[conn] = username
        joined_message = f"{username} has joined the chat!"
        sendAll(joined_message, username)

        connected = True
        while connected and server_active.is_set():
            try: 
                message_length_encoded = conn.recv(HEADER_SIZE_IN_BYTES)
                message_length_string = message_length_encoded.decode(FORMAT)
                if message_length_string:
                    message_length_int = int(message_length_string)
                    message_encoded = conn.recv(message_length_int)
                    message = message_encoded.decode(FORMAT)
                    if message != DISCONNECT_MESSAGE:
                        print (f"[{addr}] {message}")
                        sendAll(message, conn, username)
                    else:
                        connected = False
            except socket.timeout:
                pass
        
        print (f"[END CONNECTION] {addr} disconnected.")
        print (f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        left_message = f"{username} has left the chat."
        sendAll(left_message, username)
        del client_sockets[conn]
        conn.close()
    except Exception as e:
        print (f"[ERROR] {addr} {e}")
        if conn in client_sockets:
            del client_sockets[conn]
        conn.close()

def encode_message(message):
    message_encoded = message.encode(FORMAT)
    message_length = len(message_encoded)
    message_send_length = str(message_length).encode(FORMAT)
    padding_needed = HEADER_SIZE_IN_BYTES - len(message_send_length)
    # this repeats the space byte by padding needed times
    padding = b' ' * padding_needed
    padded_message_send_length = message_send_length + padding
    return padded_message_send_length , message_encoded

def send(conn, message):
    padded_message_send_length, message_encoded = encode_message(message)
    conn.send(padded_message_send_length)
    conn.send(message_encoded)

def sendAll(message, except_conn=None, username=None):
    if username:
        full_message = f"[{username}] {message}"
    else:
        full_message = message

    padded_length_encoded, message_encoded = encode_message(full_message)

    for conn in client_sockets:
        if conn != except_conn:
            conn.send(padded_length_encoded)
            conn.send(message_encoded)


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(TCP_ADDR)
    print ("[STARTING] Server is starting...")
    server.listen()
    server.settimeout(1)
    print (f"[LISTENING] Server is listening on {SERVER_IP}")
    threads = []
    server_active = threading.Event()
    server_active.set()
    try:
        while True:
            try:
                # this is a blocking command, it will wait for a new connection to the server
                conn, addr = server.accept()
                conn.settimeout(10)
                thread = threading.Thread(target=handle_client, args=(conn, addr, server_active))
                thread.start()
                threads.append(thread)
                print (f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
                client_sockets[conn] = None
            except socket.timeout:
                pass
    except KeyboardInterrupt:
        print ("[SHUTTING DOWN] Attempting to close threads.")
        server_active.clear()
        for thread in threads:
            thread.join()
        print (f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    server.close()