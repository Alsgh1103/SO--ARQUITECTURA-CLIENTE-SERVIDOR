import socket
import os
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mi_socket.bind (('localhost', 8080))
mi_socket.listen(5)
print ("Servidor encendido en el puerto 8080. Esperando...")

while True:
    conexion, direccion = mi_socket.accept()
    print('Conexion establecida, la direccion es', direccion)
    mensaje = "Hola amix"
    conexion.send(mensaje.encode('utf-8'))
    conexion.close()
