import os
import socket
import tkinter as tk
from tkinter import filedialog

# Các biến cần thiết
KEY = b"your_32_byte_aes_key_here"  # Thay bằng khóa AES 32 byte của bạn
TARGET_IP = "127.0.0.1"  # Địa chỉ IP của thiết bị nhận
TARGET_PORT = 12345  # Cổng của thiết bị nhận
MY_PORT = 12345  # Cổng của thiết bị hiện tại
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket gửi

# Hàm mã hóa (giả sử bạn đã định nghĩa)
def encrypt_message(key, message):
    # Thêm logic mã hóa AES của bạn ở đây
    return message.encode('latin1')

# Hàm giải mã (giả sử bạn đã định nghĩa)
def decrypt_message(key, encrypted_message):
    # Thêm logic giải mã AES của bạn ở đây
    return encrypted_message.decode('latin1')

# Gửi file
def send_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Đọc và mã hóa file
    with open(file_path, "rb") as f:
        file_data = f.read()
    encrypted_file_data = encrypt_message(KEY, file_data.decode('latin1'))

    # Gửi file
    sender.sendto(b"FILE:" + encrypted_file_data, (TARGET_IP, TARGET_PORT))
    chat_box.insert(tk.END, f"Bạn đã gửi file: {os.path.basename(file_path)}\n")

# Nhận file
def handle_file(data, addr):
    try:
        decrypted_file_data = decrypt_message(KEY, data)
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Lưu file nhận")
        if save_path:
            with open(save_path, "wb") as f:
                f.write(decrypted_file_data.encode('latin1'))
            chat_box.insert(tk.END, f"Đã nhận file từ {addr[0]} và lưu tại {save_path}\n")
    except:
        chat_box.insert(tk.END, f"{addr[0]}: [Không giải mã được file]\n")

# Cập nhật server nhận để xử lý file
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', MY_PORT))
    while True:
        data, addr = server.recvfrom(4096)
        try:
            if data.startswith(b'FILE:'):  # Định dạng file
                handle_file(data[5:], addr)
            else:
                msg = decrypt_message(KEY, data)
                chat_box.insert(tk.END, f"{addr[0]}: {msg}\n")
        except:
            chat_box.insert(tk.END, f"{addr[0]}: [Không giải mã được]\n")

# Tạo giao diện
window = tk.Tk()
window.title("Peer Chat")

chat_box = tk.Text(window, height=20, width=50)
chat_box.pack()

tk.Button(window, text="Gửi File", command=send_file).pack()

# Chạy server trong luồng riêng
import threading
threading.Thread(target=start_server, daemon=True).start()

# Chạy giao diện
window.mainloop()
