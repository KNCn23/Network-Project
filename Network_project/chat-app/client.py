# client.py
import socket
import threading

# İstemci bilgisi
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

nickname = input("Kullanıcı adınızı girin: ")

# İstemci soketi oluşturma ve sunucuya bağlanma
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

# Sunucudan mesaj almayı dinleyen fonksiyon
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Bağlantı sunucudan kesildi!")
            client.close()
            break

# Kullanıcıdan mesaj alıp sunucuya gönderen fonksiyon
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Mesaj alıcı iş parçacığını başlat
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Mesaj gönderici iş parçacığını başlat
write_thread = threading.Thread(target=write)
write_thread.start()
