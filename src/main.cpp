/*

In this file, we are learning about the ins-and-outs of TCP programming.

The steps to recieving network data TCP style are:

1. Create a socket
2. Bind / claim a Port
3. Listen (or don't, if you're the client)
4. Accept a connection - This creates a new socket for accepted clients
5. Receive data


---------------------------------------------
SOCKETS


What is an "Endpoint"?
- When a "socket" is created, it doesn't have an IP or port yet
- When you create a socket, you tell the kernel 2 things:
    - Address Family (AF_INET): IPv4 addresses
    - Type (SOCK_STREAM): TCP, etc


Where does streamed data get stored?
- Incoming data gets stored in the kernel memory
- When you create a socket, the kernel creates an internal data structure
    ('struct socket' or 'struct sock')
- The structure contains small chunks of kernel memory that hold
  data coming off the wire before your app reads it. It also contains
  state information (ESTABLISHED, WAITING, CLOSED), and wait queues
  (wait queues are a list of processes waiting for data to arrive on this socket)

So, the incoming data doesn't get written to a literal file, but rather
a chunk of memory handled by the kernel that acts as a virtual file.

*/


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

