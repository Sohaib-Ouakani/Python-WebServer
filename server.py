import socket
import os
import mimetypes
from datetime import datetime
import time
import threading

HOST, PORT = 'localhost', 8080
ROOT_DIR = './www'
LOG_FILE = 'log.txt'

def log_request(request, status_code, client_ip, elapsed):
    headers = request.split('\r\n')
    request_line = headers[0]
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{time}] {client_ip[0]}:{client_ip[1]} "{request_line}" {status_code} {round(elapsed * 1000)}ms\n'

    try:
        with open(LOG_FILE, 'a') as log:
            log.write(log_entry)
            print(log_entry)
    except IOError as e:
        print(f"Error writing to log file {LOG_FILE}: {e}")

def parse_request(req):
    if not req:
        return

    headers = req.split('\r\n')
    req_line = headers[0].split()

    if len(req_line) < 2:
        return None, None, None

    method, path = req_line[0], req_line[1]
    if method != 'GET':
        return None, None, None

    if path == '/':
        path = '/index.html'

    file_path = ROOT_DIR + path

    return path, method, file_path

def read_file(path):
    if os.path.isfile(path):
        try:
            with open(path, 'rb') as f:
                content = f.read()
        except IOError as err:
            print(f'erro in reading [{path}] file, code: {err}')
        return content
    else:
        return

def create_response(statuscode, mimetype, filesize, content):
    response = f"HTTP/1.1 {statuscode}\r\nContent-Type: {mimetype}\r\nContent-Length: {filesize}\r\n\r\n".encode(
            'ascii') + content
    return response

def server_reply(filepath):
    real_path = os.path.realpath(filepath)
    root_path = os.path.realpath(ROOT_DIR)

    if not real_path.startswith(root_path): #se qualcuno riesce a fare un get che va fuori dalla cartella root
        status_code = "403 Forbidden"
        content = b"<h1>403 Forbidden</h1>"
        response = create_response("403 Forbidden", "text/html", len(content), content)
        return response, status_code

    content = read_file(filepath)

    if content:
        status_code = "200 OK"
        mimetype = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        response = create_response(status_code, mimetype, len(content), content)

    else:
        filepath = ROOT_DIR + "/404.html"
        content = read_file(filepath)
        status_code = "404 Not Found"
        mimetype = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        response = create_response(status_code, mimetype, len(content), content)


    return response, status_code

def handle_request(client_socket, client_ip):
    start = time.time()

    request = client_socket.recv(1024).decode('ascii')

    path, method, filepath = parse_request(request)
    if not path:
        client_socket.close()
        return

    response, status_code = server_reply(filepath)

    client_socket.sendall(response)
    client_socket.close()

    finish = time.time()
    time_elapsed = finish - start

    log_request(request, status_code, client_ip, time_elapsed)

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Server in ascolto su http://{HOST}:{PORT}/")

        while True:
            client_socket, client_ip = server.accept()
            thread = threading.Thread(target = handle_request, args = (client_socket, client_ip))
            thread.daemon = True
            thread.start()

if __name__ == '__main__':
    run_server()
