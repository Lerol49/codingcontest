from website import create_app
import socket

app = create_app()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


local = False

if local:
    ip = "127.0.0.1"
else:
    ip = get_ip_address()


if __name__ == "__main__":
    app.run(host=ip, port=8080, debug=True)
