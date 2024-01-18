import socket
import threading

def handle_client(client_socket, address):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f'{address}: {message}')
        broadcast(message, address)
    client_socket.close()

def broadcast(message, sender_address):
    for client, address in clients:
        if address != sender_address:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Якщо виникає помилка, видаляємо клієнта
                remove_client(client, address)

def remove_client(client, address):
    if (client, address) in clients:
        clients.remove((client, address))
        print(f'{address} вийшов з чату')

# Створення TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(5)

print('Сервер чату запущено...')

# Список підключених клієнтів та їхні адреси
clients = []

while True:
    client_socket, client_address = server_socket.accept()
    print(f'Приєднався {client_address}')
    clients.append((client_socket, client_address))

    # Запуск окремого потоку для кожного клієнта
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
