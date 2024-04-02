import socket
import threading
from typing import List


def parse_input(input: bytes) -> List[str]:
    input = input.decode()
    return input.split("\r\n")


def convert_to_output(input: List[str]) -> bytes:
    output = "\r\n".join(input) + "\r\n"
    return output.encode()


def handle_request(input: bytes) -> bytes:
    # we expect requests like this:
    # GET /index.html HTTP/1.1
    # Host: localhost:4221
    # User-Agent: curl/7.64.1
    input = parse_input(input)
    method, path, version = input[0].split(" ")
    output = []
    if path == "/":
        output.append("HTTP/1.1 200 OK")
        output.append("")  # empty body
    elif len(path) >= 5 and path[:5] == "/echo":
        body = path[6:]
        output.append("HTTP/1.1 200 OK")
        output.append("Content-Type: text/plain")
        output.append(f"Content-Length: {len(body)}")
        output.append("")
        output.append(body)
    elif len(path) >= 11 and path[:11] == "/user-agent":
        body = input[2].split(": ")[1]
        output.append("HTTP/1.1 200 OK")
        output.append("Content-Type: text/plain")
        output.append(f"Content-Length: {len(body)}")
        output.append("")
        output.append(body)
    else:
        output.append("HTTP/1.1 404 Not Found")
        output.append("")
    print(output)

    return convert_to_output(output)


def handle_client(connection):
    with connection:
        while True:
            input = connection.recv(1024)
            connection.sendall(handle_request(input))
    server_socket.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, client = server_socket.accept()  # wait for client
        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()


if __name__ == "__main__":
    main()
