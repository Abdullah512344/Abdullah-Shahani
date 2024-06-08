import socket
import threading
import os

class ChunkServer:
    def __init__(self, host, port, storage_dir):
        self.host = host
        self.port = port
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def handle_client(self, conn, addr):
        print(f"Connected by {addr}")
        try:
            data = conn.recv(1024).decode()
            command_parts = data.split()
            if len(command_parts) < 2:
                raise ValueError("Invalid command format")

            command = command_parts[0]
            chunk_id = command_parts[1]

            if command == "STORE":
                self.store_chunk(conn, chunk_id)
            elif command == "RETRIEVE":
                self.retrieve_chunk(conn, chunk_id)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            conn.close()

    def store_chunk(self, conn, chunk_id):
        print(f"Storing chunk {chunk_id}")
        chunk_data = conn.recv(1024 * 1024)  
        chunk_id = chunk_id.split(':')[0]
        chunk_path = os.path.join(self.storage_dir, chunk_id)
        with open(chunk_path, 'wb') as f:
            f.write(chunk_data)
        print(f"Stored chunk {chunk_id}")

    def retrieve_chunk(self, conn, chunk_id):
        print(f"Retrieving chunk {chunk_id}")
        chunk_id = chunk_id.split(':')[0]  # Ensure proper chunk_id
        chunk_path = os.path.join(self.storage_dir, chunk_id)
        if os.path.exists(chunk_path):
            with open(chunk_path, 'rb') as f:
                conn.sendall(f.read())
            print(f"Retrieved chunk {chunk_id}")
        else:
            conn.sendall(b"ERROR: Chunk not found")
            print(f"Chunk {chunk_id} not found")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Chunk server started on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 chunk_server.py <host> <port> <storage_dir>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    storage_dir = sys.argv[3]

    server = ChunkServer(host, port, storage_dir)
    server.start()
