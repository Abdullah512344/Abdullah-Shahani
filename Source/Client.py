import socket
import sys

def send_to_master(server_address, message, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_address)
        s.sendall(message.encode())
        s.sendall(data)
        response = s.recv(1024).decode()
        return response

def upload_file(master_address, filename, filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    message = f"CREATE {filename}"
    response = send_to_master(master_address, message, data)
    print(response)

def list_files(master_address):
    message = "LIST"
    response = send_to_master(master_address, message, b'')
    print("Files on the system:")
    print(response)

def download_file(master_address, filename, dest_filepath):
    message = f"GET_CHUNKS {filename}"
    response = send_to_master(master_address, message, b'')
    chunks = response.split()
    with open(dest_filepath, 'wb') as f:
        for chunk in chunks:
            chunk_id = chunk
            host, port = "localhost", 50051  # Local ports that are 50051,50052,50053
            chunk_data = retrieve_chunk_from_server(host, port, chunk_id)
            f.write(chunk_data)

def retrieve_chunk_from_server(host, port, chunk_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(f"RETRIEVE {chunk_id}".encode())
        chunk_data = s.recv(1024)
        return chunk_data

if __name__ == '__main__':
    master_address = ('localhost', 50050)
    command = sys.argv[1]
    if command == 'upload':
        filename = sys.argv[2]
        filepath = sys.argv[3]
        upload_file(master_address, filename, filepath)
    elif command == 'list':
        list_files(master_address)
    elif command == 'download':
        filename = sys.argv[2]
        dest_filepath = sys.argv[3]
        download_file(master_address, filename, dest_filepath)
