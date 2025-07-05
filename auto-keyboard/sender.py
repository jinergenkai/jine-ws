import socket

def main():
    ip = input("Nhập IP Máy B: ").strip()
    port = 12345
    text = input("Nhập nội dung muốn gửi: ")
    s = socket.socket()
    try:
        s.connect((ip, port))
        s.send(text.encode("utf-8"))
        print("Đã gửi thành công!")
    except Exception as e:
        print("Lỗi khi gửi:", e)
    finally:
        s.close()

if __name__ == "__main__":
    main()