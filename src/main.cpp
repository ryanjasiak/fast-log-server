#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <cstdlib>
#include <thread>

#include "log_entry.hpp"

void process_client(int data_sock) {

    char buffer[512];
    while (true) {

        int bytes_read = recv(data_sock, buffer, sizeof(buffer) - 1, 0);
        if (bytes_read > 0)
        {
            buffer[bytes_read] = '\0';
            std::cout << "Received: " << buffer << std::endl;
        } else {
            close(data_sock);
            return;
        }
    }

    close(data_sock);
}

int main() {
    const char* SOCKET_PATH = std::getenv("UDS_SOCKET");
    int listen_sock, data_sock;
    struct sockaddr_un server_addr;

    // Step 1: Create the socket
    listen_sock = socket(AF_UNIX, SOCK_STREAM, 0);
    if (listen_sock == -1) {
        perror("socket err");
    }

    unlink(SOCKET_PATH);

    // Step 2: Bind socket to an address file (a file path)
    memset(&server_addr, 0, sizeof(struct sockaddr_un));
    server_addr.sun_family = AF_UNIX;

    strncpy(server_addr.sun_path, SOCKET_PATH, sizeof(server_addr.sun_path) - 1);

    if (bind(listen_sock, (const struct sockaddr*)&server_addr, sizeof(struct sockaddr_un)) == -1) {
        perror("bind error");
        exit(EXIT_FAILURE);
    }

    std::cout << "Server listening on " << SOCKET_PATH << std::endl;

    if (listen(listen_sock, 20) == -1) {
        perror("listen error");
        exit(EXIT_FAILURE);
    }

    while (true) {

        data_sock = accept(listen_sock, NULL, NULL);
        if (data_sock != -1)
        {
            std::cout << "Client connected" << std::endl;
            std::thread(process_client, data_sock).detach();
        }

    }
    close(listen_sock);
    unlink(SOCKET_PATH);

}

