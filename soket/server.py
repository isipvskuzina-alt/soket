import socket
import threading

clients = []
clients_lock = threading.Lock()


def broadcast(message, sender_socket=None):

    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    pass


def handle_client(client_socket, client_addr):
    print(f"Клиент {client_addr} подключён")

    welcome_msg = f"Добро пожаловать в чат, {client_addr}!\n"
    client_socket.send(welcome_msg.encode('utf-8'))

    broadcast(f"{client_addr} присоединился к чату!", client_socket)

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f'От {client_addr} пришло: {message}')

            broadcast(f"{client_addr}: {message}", client_socket)

        except:
            break

    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

    client_socket.close()
    print(f'Клиент {client_addr} отключился')

    broadcast(f"{client_addr} покинул чат!")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen(5)

    print('Сервер запущен на 127.0.0.1:5000')
    print('Ожидание подключения клиентов...\n')

    while True:
        client_socket, client_addr = server_socket.accept()

        with clients_lock:
            clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    start_server()