import socket
import threading

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

# Створення TCP-клієнта
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

# Запуск потоку для отримання повідомлень
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Введення та надсилання повідомлень
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))

# Закриття з'єднання
client_socket.close()
