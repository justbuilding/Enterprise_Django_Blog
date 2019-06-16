# coding=utf-8
import socket
import sys


reload(sys)
# 解决len(body.encode())报的错'ascii' codec can't decode byte 0xef in position 45: ordinal not in range(128)
sys.setdefaultencoding('utf-8')


# GMT = 北京时间 - 八小时
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello, world! <h1> from the5fire 《Django企业开发实践》<h1>'''

response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sun 16 June 2019 13:11:00 GMT',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Length: {}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print(request)
    conn.send(response.encode())  # response转为bytes后传输
    conn.close()


def main():
    # socket.AF_INET 用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM 用于基于TCP的流式socket通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用，保证我们每次按ctrl c之后能快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    serversocket.bind(('127.0.0.1',8000))
    serversocket.listen(5)  # 设置backlog--socket连接最大排队数量
    print('http://127.0.0.1:8000')

    try:
        while True:
            conn, address = serversocket.accept()
            handle_connection(conn, address)
    finally:
        serversocket.close()


if __name__ ==  '__main__':
    main()
