# server.py
import socket
import os


def start_vulnerable_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))  # Server 9999-portda ishlaydi
    server_socket.listen(1)

    print("Server 9999-portda ishga tushdi. Clientni kutmoqda...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client ulandi: {addr}")

        # Clientdan ma'lumot qabul qilish
        data = client_socket.recv(1024).decode()
        print(f"Qabul qilingan buyruq: {data}")

        # Zaiflik: Kiritilgan ma'lumotni tekshirmasdan ishga tushirish
        try:
            result = os.popen(data).read()  # Bu RCE zaifligini keltirib chiqaradi
            client_socket.send(result.encode())
        except Exception as e:
            client_socket.send(f"Xato: {str(e)}".encode())

        client_socket.close()


if __name__ == "__main__":
    start_vulnerable_server()