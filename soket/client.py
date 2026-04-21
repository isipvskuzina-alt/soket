import socket
import threading
import sys


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\r{message}")
            print("Вы: ", end="", flush=True)
        except:
            print("\nСоединение с сервером потеряно")
            break


def send_messages(client_socket):
    while True:
        try:
            message = input()
            if message.lower() == '/quit':
                print("Отключение от чата...")
                break
            if message:
                client_socket.send(message.encode('utf-8'))
        except:
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(("127.0.0.1", 5000))
        print("Подключено к чат-серверу")
        print("Для выхода введите /quit\n")
    except:
        print("Не удалось подключиться к серверу")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.daemon = True
    send_thread.start()

    send_thread.join()

    client_socket.close()
    print("Вы вышли из чата")


if __name__ == "__main__":
    start_client()