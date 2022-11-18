from main import tiny, long
import socket

HDRS = 'HTTP/1.1 200 0K\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('127.0.0.1', 2003))
        server.listen(10)
        while True:
            client_socket, adress = server.accept()
            print('Working...')
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            if len(data.split()) < 2:
                return None
            if data.split()[1] == "/" or data.split()[1] == "/favicon.ico":
                content = load_page_from_get_request(data)
                client_socket.send(content)
                # client_socket.send(b'HTTP/1.1 301 Moved Permanently\nLocation: https://www.google.com/')
                client_socket.shutdown(socket.SHUT_WR)
            elif data.split()[1][1] == "?":
                data = data.split()[1]
                link = data[7:]
                url = tiny(link)
                client_socket.send(HDRS.encode("utf-8") + f"127.0.0.1:2003/{url}".encode("utf-8"))
            else:
                data = data.split()[1][1:]
                url = long(data)
                client_socket.send(f'HTTP/1.1 301 Moved Permanently\nLocation: https://www.{url}/'.encode('utf-8'))


    except KeyboardInterrupt:
        server.close()
        print("Closing...")


def load_page_from_get_request(request_data):
    path = request_data.split(' ')
    if len(path) > 1:
        with open("views/home.html", "rb") as file:
            response = file.read()
        return HDRS.encode("utf-8") + response
    else:
        return HDRS.encode("utf-8")


if __name__ == "__main__":
    start_server()
