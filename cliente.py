import socket

direccion_ip_servidor = input("IP del servidor (Enter para localhost): ")
if direccion_ip_servidor == "":
    direccion_ip_servidor = "127.0.0.1"

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((direccion_ip_servidor, 8080))

peticion_inicial = "index.txt"
cliente_socket.send(peticion_inicial.encode('utf-8'))
respuesta_servidor = cliente_socket.recv(4096).decode('utf-8')
print("\n" + respuesta_servidor + "\n")

while True:
    comando_usuario = input("-> ")
    
    if comando_usuario.strip() == "":
        continue
        
    cliente_socket.send(comando_usuario.encode('utf-8'))
    
    if comando_usuario == ">END":
        break
        
    respuesta_servidor = cliente_socket.recv(4096).decode('utf-8')
    print("\n" + respuesta_servidor + "\n")

cliente_socket.close()