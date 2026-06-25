import socket
import os

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.bind(('0.0.0.0', 8080))
servidor_socket.listen(5)
print("Servidor listo y esperando conexiones en el puerto 8080...")

while True:
    conexion_cliente, direccion_cliente = servidor_socket.accept()
    print(f"\n[+] Nuevo cliente conectado desde: {direccion_cliente[0]}")
    while True:
        try:
            datos_recibidos = conexion_cliente.recv(1024).decode('utf-8')
            if not datos_recibidos:
                break
            
            peticion = datos_recibidos.strip()
            print(f"[{direccion_cliente[0]}] solicitó: {peticion}")
            
            if peticion == ">END":
                break
            
            if peticion == ">Home" or peticion == "":
                peticion = "index.txt"
                
            if peticion.startswith('<') and peticion.endswith('>'):
                peticion = peticion[1:-1]
                
            ruta_solicitada = os.path.abspath(peticion)
            directorio_base = os.path.abspath('.')
            
            if not ruta_solicitada.startswith(directorio_base):
                conexion_cliente.send("Acceso denegado\n".encode('utf-8'))
                continue
                
            if os.path.isfile(peticion):
                with open(peticion, 'r', encoding='utf-8') as archivo:
                    contenido_archivo = archivo.read()
                conexion_cliente.send(contenido_archivo.encode('utf-8'))
            else:
                conexion_cliente.send("Archivo no encontrado\n".encode('utf-8'))
        except Exception:
            break
    conexion_cliente.close()
