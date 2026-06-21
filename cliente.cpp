#include <iostream>
#include <winsock2.h> // Librería principal para Sockets en Windows

#pragma comment(lib, "ws2_32.lib") // Instrucción para enlazar la librería de red

// Comando de compilación en windows (CMD):  g++ cliente.cpp -o cliente.exe -lws2_32

int main() {
    // 1. Inicializar Winsock (Requisito de Windows)
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    // 2. Crear socket
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);

    // 3. Configurar dirección
    sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(8080);
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // 4. Conectar
    connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    std::cout<<"conexion establecida con el servidor ..."<<std::endl;

    // 5. Enviar y recibir
    char buffer[1024] = {0};
    std::string nombre_archivo;
    std::cout << "Nombre del archivo: ";
    std::cin >> nombre_archivo;
    
    send(sock, nombre_archivo.c_str(), nombre_archivo.length(), 0);
    recv(sock, buffer, 1024, 0);

    std::cout << "Respuesta:\n" << buffer << std::endl;

    // 6. Limpieza
    closesocket(sock);
    WSACleanup();
    return 0;
}