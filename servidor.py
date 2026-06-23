import socket
import os
import re
from urllib.parse import unquote

def enviar_404(conexion, nombre_archivo):
    mensaje_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
</head>
<body>
    <h1>404 Not Found</h1>
    <p>El archivo <strong>{nombre_archivo}</strong> no existe en el servidor o no es accesible.</p>
</body>
</html>"""
    cuerpo = mensaje_html.encode('utf-8')
    cabecera = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(cuerpo)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    conexion.sendall(cabecera.encode('utf-8') + cuerpo)

mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mi_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mi_socket.bind(('localhost', 8080))
mi_socket.listen(5)
print("Servidor Web HTTP encendido en http://localhost:8080")
print("Esperando conexiones de navegadores...")

while True:
    try:
        conexion, direccion = mi_socket.accept()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error al aceptar conexión: {e}")
        continue

    peticion = b""
    try:
        while b"\r\n\r\n" not in peticion:
            datos = conexion.recv(1024)
            if not datos:
                break
            peticion += datos
    except Exception as e:
        print(f"Error al recibir datos: {e}")
        conexion.close()
        continue

    if not peticion:
        conexion.close()
        continue

    peticion_texto = peticion.decode('utf-8', errors='ignore')
    lineas = peticion_texto.split('\r\n')
    if not lineas or not lineas[0]:
        conexion.close()
        continue

    partes = lineas[0].split(' ')
    if len(partes) < 2:
        conexion.close()
        continue

    metodo = partes[0]
    ruta = partes[1]

    ruta = unquote(ruta.split('?')[0])

    print(f"[{direccion[0]}:{direccion[1]}] - Petición: {metodo} {ruta}")

    if metodo != 'GET':
        enviar_404(conexion, ruta)
        conexion.close()
        continue

    if ruta == '/':
        nombre_archivo = 'index.TXT'
    else:
        nombre_archivo = ruta.lstrip('/')

    if not nombre_archivo.lower().endswith('.txt'):
        print(f" -> Denegado (extensión no permitida o no válida)")
        enviar_404(conexion, nombre_archivo)
        conexion.close()
        continue

    directorio_base = os.path.abspath('.')
    ruta_completa = os.path.abspath(os.path.join(directorio_base, nombre_archivo))
    if not ruta_completa.startswith(directorio_base):
        print(f" -> Denegado (intento de directory traversal)")
        enviar_404(conexion, nombre_archivo)
        conexion.close()
        continue

    archivo_real = None
    if os.path.exists(nombre_archivo) and os.path.isfile(nombre_archivo):
        archivo_real = nombre_archivo
    else:
        for entrada in os.listdir('.'):
            if entrada.lower() == nombre_archivo.lower() and os.path.isfile(entrada):
                archivo_real = entrada
                break

    if archivo_real and os.path.exists(archivo_real):
        try:
            with open(archivo_real, 'r', encoding='utf-8', errors='ignore') as archivo:
                contenido = archivo.read()

            contenido_procesado = re.sub(
                r'<([^>]+\.[tT][xX][tT])>',
                r'<a href="/\1">\1</a>',
                contenido
            )

            contenido_procesado = contenido_procesado.replace('\r\n', '<br>').replace('\n', '<br>')

            cuerpo = contenido_procesado.encode('utf-8')
            cabecera = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(cuerpo)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            conexion.sendall(cabecera.encode('utf-8') + cuerpo)
            print(f" -> 200 OK ({archivo_real})")
        except Exception as e:
            print(f" -> Error al procesar archivo: {e}")
            enviar_404(conexion, nombre_archivo)
    else:
        print(f" -> 404 Not Found")
        enviar_404(conexion, nombre_archivo)

    conexion.close()

mi_socket.close()
