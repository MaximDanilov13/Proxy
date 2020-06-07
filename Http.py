import socket


class HttpWorker:

    @staticmethod
    def create_connection_get(client, config):
        from start_proxy import logger
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Initialize socket for http: {0}".format(server))
        try:
            server.connect((config["host"], config["port"]))
            logger.info("Connect to {0}, from port {1}".format(config["host"], config["port"]))
            server.send(config["data"])
            reply = server.recv(8192)
            data = reply
            server.settimeout(0.2)
            while len(reply):
                try:
                    logger.info("Receive data from server and sending to client: {0}".format(reply))
                    client.send(reply)
                    data += reply
                    reply = server.recv(8192)
                except socket.timeout:
                    break
            print(len(data))
            client.send(b"\r\n\r\n")
            logger.info("Close connection between {0} and {1}".format(socket.socket.getsockname(server),
                                                                      socket.socket.getsockname(client)))
            server.close()
            client.close()
            return
        except Exception as e:
            server.close()
            client.close()
            print(e)
            return
