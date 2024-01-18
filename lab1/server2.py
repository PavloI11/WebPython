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

# Прийом та відправка даних з затримкою та перевіркою
data = client_socket.recv(1024).decode('utf-8')
time.sleep(5)  # Затримка 5 секунд
client_socket.send(f'Server received: {data}'.encode('utf-8'))

# Відлунювання отриманого повідомлення
print(f'Отримано: {data}')

# Закриття з'єднання
client_socket.close()
server_socket.close()
