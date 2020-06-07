class DataParser:
    @staticmethod
    def parse_method(data):
        lines = data.splitlines()
        first_line = lines[0]
        method = first_line.split()[0]
        return method

    @staticmethod
    def parse_server_port_get(data):
        return 80

    @staticmethod
    def parse_host_get(data):
        lines = data.splitlines()
        host = lines[1].split()[1]
        return host

    @staticmethod
    def create_config(data):
        if len(data) == 0:
            return
        method = DataParser.parse_method(data)
        if method == b'GET':
            host = DataParser.parse_host_get(data)
            port = DataParser.parse_server_port_get(data)
            parse_data = data
        elif method == b'CONNECT':
            host, port = DataParser.parse_server_host_connect(data)
            parse_data = DataParser.parse_data_connect(data)
        else:
            return {}
        config = {
            "port": port,
            "host": host,
            "method": method,
            "data": parse_data
        }
        return config

    @staticmethod
    def parse_server_host_connect(data):
        lines = data.splitlines()
        line = lines[len(lines) - 2]
        host_with_port = line.split()[1]
        host = host_with_port[:len(host_with_port)-4]
        port = host_with_port[-3:]
        return host, int(port)

    @staticmethod
    def parse_data_connect(data):
        lines = data.splitlines()
        while lines[len(lines)-1] == '':
            lines.remove('')
        token = lines[0].split()
        url = token[1]
        url_pos = url.find(b"://")
        if url_pos != -1:
            url = url[(url_pos + 3):]
        path_pos = url.find(b"/")
        if path_pos == -1:
            path_pos = len(url)
        token[1] = url[path_pos:]
        lines[0] = b' '.join(token)
        new_data = b"\r\n".join(lines) + b'\r\n\r\n'
        return new_data


class DataReceiver:

    @staticmethod
    def receive_data(sock):
        sock.settimeout(0.3)
        data = b''
        try:
            reply = sock.recv(8192)
            data += reply
            while len(reply):
                reply = sock.recv(8192)
                data += reply
        finally:
            return data
