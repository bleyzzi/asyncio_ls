import socket

from select import select

to_monitor = []


def accept_connection(server_socket):
    client_socket, _addr = server_socket.accept()
    print('Connection from', _addr)

    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = 'Hello world'.encode()
        client_socket.send(response)
    else:
        to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    to_monitor.append(server_socket)
    event_loop()
