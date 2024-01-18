import socket

# Створення TCP-клієнта
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

# Введення тексту від користувача
message = input('Введіть текст для відправки на сервер: ')

# Відправлення даних на сервер
client_socket.send(message.encode('utf-8'))

# Закриття з'єднання
client_socket.close()
