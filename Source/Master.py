import socket
import threading
import os

class MasterServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.files = {}  # filename -> list of chunks
        self.chunk_servers = ["localhost:50051", "localhost:50052", "localhost:50053"]  # Addresses of chunk servers

    def handle_client(self, conn, addr, filepath):
        print(f"Connected by {addr}")
        data = conn.recv(1024).decode()
        command, *args = data.split()
        if command == "CREATE":
            self.create_file(conn, args, filepath)
        elif command == "LIST":
            self.list_files(conn)
        elif command == "GET_CHUNKS":
            self.get_chunks(conn, args)
        conn.close()

    def create_file(self, conn, args, filepath):
        filename = args[0]
        with open(filepath, 'rb') as f:
            data = f.read()
        chunk_size = 1024  # 1KB for simplicity
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        self.files[filename] = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk{i}"
            self.files[filename].append(chunk_id)
            chunk_servers = self.chunk_servers[i % len(self.chunk_servers):] + self.chunk_servers[:i % len(self.chunk_servers)]
            self.send_chunk_to_servers(chunk_servers[:2], chunk_id, chunk)  # Send to first 2 servers for replication
        conn.sendall(b"File created successfully")

    def list_files(self, conn):
        files_list = "\n".join(self.files.keys())
        conn.sendall(files_list.encode())

    def get_chunks(self, conn, args):
        filename = args[0]
        chunks_list = " ".join(self.files.get(filename, []))
        conn.sendall(chunks_list.encode())

    def send_chunk_to_servers(self, servers, chunk_id, chunk):
        for server in servers:
            host, port = server.split(':')
            self.send_chunk_to_server(host, int(port), chunk_id, chunk)

    def send_chunk_to_server(self, host, port, chunk_id, chunk):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(f"STORE {chunk_id}".encode())
            s.sendall(chunk)

    def start(self, filepath):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print("Master server started, waiting for connections...")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr, filepath)).start()

if __name__ == "__main__":
    master = MasterServer('localhost', 50050)
    filepath = 'input/input.txt'
    master.start(filepath)
