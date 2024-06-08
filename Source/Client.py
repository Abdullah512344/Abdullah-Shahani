import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import os
import time 
class DFSClient:
    def __init__(self, master):
        self.master = master
        self.master.title("DFS Client")

        self.label = tk.Label(master, text="Distributed File System Client")
        self.label.pack()

        self.upload_button = tk.Button(master, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.download_button = tk.Button(master, text="Download File", command=self.download_file)
        self.download_button.pack()

        self.file_list_label = tk.Label(master, text="Files in DFS:")
        self.file_list_label.pack()

        self.file_listbox = tk.Listbox(master)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        self.refresh_button = tk.Button(master, text="Refresh File List", command=self.refresh_file_list)
        self.refresh_button.pack()

        self.master_address = ('192.168.145.128', 50050)  # IP and port of the master server
        self.refresh_file_list()

    def upload_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                file_data = f.read()
            file_size = len(file_data)
            print(f"File size reported during creation: {file_size}")
            message = f"CREATE {filename} {file_size}"
            response = self.send_to_master(message, file_data)
            messagebox.showinfo("Upload", response.decode())
            self.refresh_file_list()
            

    def download_file(self):
        selected_files = self.file_listbox.curselection()
        if selected_files:
            filename = self.file_listbox.get(selected_files[0])
            message = f"DOWNLOAD {filename}"
            file_data = self.send_to_master(message)
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename)
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(file_data)
                messagebox.showinfo("Download", f"{filename} downloaded successfully.")
        else:
            messagebox.showwarning("Download", "Please select a file to download.")

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        message = "LIST"
        response = self.send_to_master(message)
        file_list = response.decode().split("\n")
        for file in file_list:
            if file:
                self.file_listbox.insert(tk.END, file)

    def send_to_master(self, message, data=b''):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.master_address)
            s.sendall(message.encode())
            if data:
                time.sleep(5)
                s.sendall(data)
       
            response = s.recv(1024 * 1024)
            return response

if __name__ == "__main__":
    root = tk.Tk()
    client = DFSClient(root)
    root.mainloop()
