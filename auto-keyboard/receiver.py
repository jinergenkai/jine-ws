import socket
import pyautogui

def main():
    host = "0.0.0.0"
    port = 12345
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print(f"Đang lắng nghe trên cổng {port}...")

    while True:
        conn, addr = s.accept()
        print(f"Nhận kết nối từ {addr}")
        data = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk
        text = data.decode("utf-8")
        if text:
            print(f"Gõ: {text}")
            pyautogui.typewrite(text)
        conn.close()

if __name__ == "__main__":
    main()