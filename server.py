from main import tiny, long
import socket

HDRS = 'HTTP/1.1 200 0K\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('127.0.0.1', 2000))
        server.listen(10)
        while True:
            client_socket, adress = server.accept()
            print('Working...')
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            if data.split()[0] == "GET":
                content = load_page_from_get_request(data)
                client_socket.send(content)
                client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print("Closing...")


def load_page_from_get_request(request_data):
    path = request_data.split(' ')
    if len(path) > 1:
        path = path[1].strip('/')
        if path == "":
            with open("views/home.html", "rb") as file:
                response = file.read()
            return HDRS.encode("utf-8") + response
        print(long(path))
        return HDRS.encode("utf-8")
    else:
        return HDRS.encode("utf-8")


if __name__ == "__main__":
    start_server()
