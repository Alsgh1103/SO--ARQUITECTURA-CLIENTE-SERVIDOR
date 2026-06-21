import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
client.connect(('127.0.0.1', 8080))
print("conexion establecida con el servidor ...")

nombre = input("Archivo a solicitar: ")
client.send(nombre.encode('utf-8'))
    
respuesta = client.recv(1024).decode('utf-8')
print(f"Respuesta del servidor:\n{respuesta}")
    
client.close()