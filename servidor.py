import socket
import os
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mi_socket.bind (('localhost', 8080))
mi_socket.listen(5)
print ("Servidor encendido en el puerto 8080. Esperando...")

while True:
    conexion, direccion = mi_socket.accept()
    print(f"Conexion establecida, la direccion: {direccion}")
    nombre_archivo = conexion.recv(1024).decode('utf-8').strip()
    if not nombre_archivo:
        conexion.close()
        continue
    print(f"El cliente ha solicitado leer:{nombre_archivo}")
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

        conexion.send(contenido.encode('utf-8'))
        print("Archivo enviado con éxito")
    else:
        mensaje_error = f"ERROR: El archivo '{nombre_archivo}' no existe en el servidor"
        conexion.send(mensaje_error.encode('utf-8'))
    conexion.close()        
