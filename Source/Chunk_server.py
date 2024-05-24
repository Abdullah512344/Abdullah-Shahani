import socket
import threading
import os

class ChunkServer:
    def __init__(self, host, port, chunk_dir):
        self.host = host
        self.port = port
        self.chunk_dir = chunk_dir
        if not os.path.exists(chunk_dir):
            os.makedirs(chunk_dir)

    def handle_client(self, conn, addr):
        print(f"Connected by {addr}")
        data = conn.recv(1024).decode()
        command, *args = data.split()
        if command == "STORE":
            self.store_chunk(conn, args)
        elif command == "RETRIEVE":
            self.retrieve_chunk(conn, args)
        conn.close()

    def store_chunk(self, conn, args):
        chunk_id = args[0]
        chunk_data = conn.recv(1024)
        with open(os.path.join(self.chunk_dir, chunk_id), 'wb') as f:
            f.write(chunk_data)
        conn.sendall(b"Chunk stored successfully")

    def retrieve_chunk(self, conn, args):
        chunk_id = args[0]
        with open(os.path.join(self.chunk_dir, chunk_id), 'rb') as f:
            chunk_data = f.read()
        conn.sendall(chunk_data)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print("Chunk server started, waiting for connections...")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    chunk_dir = sys.argv[2]
    chunk_server = ChunkServer('localhost', port, chunk_dir)
    chunk_server.start()
