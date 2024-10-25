from twisted.internet import reactor, protocol, endpoints


class Client(protocol.DatagramProtocol):
    def __init__(self):
        reactor.callInThread(self.send_data)

    def datagramReceived(self, data, addr):
        data = data.decode("utf-8")
        print(data)

    def send_data(self):
        while True:
            message = input()
            self.transport.write(message.encode("utf-8"), ("127.0.0.1", 1234))
            if message == "!Q":
                reactor.stop()
                break


class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Client()

if __name__ == "__main__":
    reactor.listenUDP(0, Client())  # 0 means Pick any available port
    reactor.run()