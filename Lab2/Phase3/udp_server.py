from twisted.internet import reactor, protocol, endpoints

class Server(protocol.DatagramProtocol):
    def __init__(self, users):
        self.users = users      # Key= addr, value = name

    def datagramReceived(self, data, addr):
        message = data.decode("utf-8")
        if addr not in self.users:
            self.users[addr] = message
            print (f"A new connection has been made. Connection name: <{self.users[addr]}>")
            self.transport.write(f"Welcome to the chat <{self.users[addr]}>. Please type !Q to quit.".encode("utf-8"), addr)
            self.broadcast(f"<{self.users[addr]}> has entered the chat", exclude=addr)
        elif message == "!Q":
            print(f"<{self.users[addr]}> left the chat.")
            self.broadcast(f"<{self.users[addr]}> has left the chat", exclude=addr)
            del self.users[addr]
        else: 
            print(f"<{self.users[addr]}>: " + message)
            self.broadcast(f"<{self.users[addr]}>: " + message, exclude=addr)

    def broadcast(self, message, exclude=None):
        for addr, name in self.users.items():
            if addr!= exclude:
                self.transport.write(message.encode("utf-8"), addr)
    

if __name__ == "__main__":
    reactor.listenUDP(1234, Server({}))
    reactor.run()


    
