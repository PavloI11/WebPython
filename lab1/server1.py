import socket
import time

# Створення TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(1)

print('Сервер готовий приймати з\'єднання...')

# Прийом з'єднання від клієнта
client_socket, client_address = server_socket.accept()
print(f'З\'єднано з {client_address}')

# Прийом даних від клієнта та їх виведення
data = client_socket.recv(1024).decode('utf-8')
print(f'Отримано: {data}')

# Виведення часу отримання
print(f'Час отримання: {time.strftime("%H:%M:%S")}')

# Закриття з'єднання
client_socket.close()
server_socket.close()
