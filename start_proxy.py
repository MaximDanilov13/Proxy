import select
import socket
import sys
import logging
from Data import DataParser, DataReceiver
from Http import HttpWorker
from Https import HttpsWorker
import traceback


logging.basicConfig(filename="logs.log", filemode="w", level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger("log")


def process_request(sock, data, dict_sockets_connection, actual_socket):
    config = DataParser.create_config(data)
    logger.info("Parse data and create connection")
    if len(data) == 0 or len(config) == 0:
        sock.close()
        return
    logger.info("Config with data: {0}".format(config))
    if config["method"] == b'GET':
        HttpWorker.create_connection_get(sock, config)
        sock.close()
    if config["method"] == b'CONNECT':
        HttpsWorker.create_connection_connect(sock, config, dict_sockets_connection, actual_socket)


def main():
    dict_sockets_connections = {}
    actual_socket = set()
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", 8080))
        logger.info("Bind listening socket to port 8080")
        server_socket.listen(200)
        actual_socket.add(server_socket)
    except Exception as e:
        print(e, traceback.format_exc())
        sys.exit(e)
    while True:
        try:
            act_soc, _, _ = select.select(actual_socket, [], [])
            for sock in act_soc:
                if sock is server_socket:
                    client, addr = server_socket.accept()
                    logger.info("Receive data from {0}".format(socket.socket.getsockname(client)))
                    data = DataReceiver.receive_data(client)
                    process_request(client, data, dict_sockets_connections, actual_socket)
                else:
                    logger.info("Receive data from {0}".format(socket.socket.getsockname(sock)))
                    data = DataReceiver.receive_data(sock)
                    if len(data) == 0:
                        continue
                    else:
                        logger.info("Send data to {0}".format(socket.socket.getsockname(dict_sockets_connections[sock])))
                        dict_sockets_connections[sock].send(data)
        except Exception as e:
            print(e)
            sys.exit(e)
            client.close()


if __name__ == '__main__':
    main()
