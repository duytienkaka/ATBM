from aes_utils import generate_key, save_key

key = generate_key()
save_key(key)
print("Đã tạo khóa AES và lưu vào aes.key")
