import socket
import threading
import time

class MasterServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.files = {}  # filename -> list of chunks
        self.chunk_servers = ["192.168.145.128:50054", "192.168.145.128:50052"]  # Addresses of chunk servers

    def handle_client(self, conn, addr):
        print(f"Connected by {addr}")
        try:
            data = conn.recv(1024).decode()
            parts = data.split()
            command = parts[0]

            if command == "CREATE":
                filename = parts[1]
                size = int(parts[2])
                file_data = conn.recv(size)
                self.create_file(conn, filename, file_data)
            elif command == "LIST":
                self.list_files(conn)
            elif command == "GET_CHUNKS":
                filename = parts[1]
                self.get_chunks(conn, filename)
            elif command == "DOWNLOAD":
                filename = parts[1]
                self.download_file(conn, filename)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            conn.close()

    def create_file(self, conn, filename, data):
        print(f"Creating file {filename} with data of size {len(data)} bytes")
        
        # Adjust the chunk size
        chunk_size = (len(data) + len(self.chunk_servers) - 1) // len(self.chunk_servers)
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        self.files[filename] = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk{i}"
            self.files[filename].append(chunk_id)
            for server in self.chunk_servers:
                self.send_chunk_to_server(server, chunk_id, chunk)  # Send chunk to all servers

        # Send the data to the client
        conn.sendall(b"File created successfully")

    def list_files(self, conn):
        files_list = "\n".join(self.files.keys())
        conn.sendall(files_list.encode())

    def get_chunks(self, conn, filename):
        chunks_list = " ".join(self.files.get(filename, []))
        conn.sendall(chunks_list.encode())

    def send_chunk_to_server(self, server, chunk_id, chunk):
        host, port = server.split(':')
        threading.Thread(target=self.send_chunk_to_server_thread, args=(host, int(port), chunk_id, chunk)).start()

    def send_chunk_to_server_thread(self, host, port, chunk_id, chunk):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                full_message = f"STORE {chunk_id} {len(chunk)}".encode()
                s.sendall(full_message)
                time.sleep(0.1)  # Add delay to ensure data is sent properly
                s.sendall(chunk)
                print(f"Sent chunk {chunk_id} to {host}:{port}")
        except Exception as e:
            print(f"Error sending chunk {chunk_id} to {host}:{port}: {e}")

    def download_file(self, conn, filename):
        if filename not in self.files:
            conn.sendall(b"ERROR: File not found")
            return

        combined_data = b""
        for chunk_id in self.files[filename]:
            chunk_data = self.retrieve_chunk(chunk_id)
            if chunk_data is not None:
                combined_data += chunk_data

        conn.sendall(combined_data)

    def retrieve_chunk(self, chunk_id):
        for server in self.chunk_servers:
            host, port = server.split(':')
            chunk_data = self.retrieve_chunk_from_server(host, int(port), chunk_id)
            if chunk_data is not None:
                return chunk_data
        return None

    def retrieve_chunk_from_server(self, host, port, chunk_id):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(f"RETRIEVE {chunk_id}".encode())
                chunk_data = s.recv(1024 * 1024)  # Adjust buffer size as needed
                if chunk_data.startswith(b"ERROR"):
                    return None
                return chunk_data
        except Exception as e:
            print(f"Error retrieving chunk {chunk_id} from {host}:{port}: {e}")
            return None

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print("Master server started, waiting for connections...")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    master = MasterServer('0.0.0.0', 50050)  # Listen on all interfaces
    master.start()
