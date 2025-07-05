import tkinter as tk
from tkinter import scrolledtext
import socket

class ChatSender:
    def __init__(self, master):
        self.master = master
        master.title("Sender Chat GUI")

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.text_input = tk.Text(master, width=40, height=4)
        self.text_input.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
        self.text_input.bind("<Control-Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send (Ctrl+Enter)", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))

        self.ip_entry = tk.Entry(master, width=18)
        self.ip_entry.pack(side=tk.LEFT, padx=(0,5), pady=(0,10))
        self.ip_entry.insert(0, "IP_MAY_B")

        self.port_entry = tk.Entry(master, width=6)
        self.port_entry.pack(side=tk.LEFT, padx=(0,10), pady=(0,10))
        self.port_entry.insert(0, "12345")

    def send_message(self, event=None):
        msg = self.text_input.get("1.0", tk.END).rstrip("\n")
        ip = self.ip_entry.get().strip()
        port = int(self.port_entry.get().strip())
        if msg and ip:
            try:
                s = socket.socket()
                s.connect((ip, port))
                s.send(msg.encode("utf-8"))
                s.close()
                self.append_chat(f"Bạn:\n{msg}")
                self.text_input.delete("1.0", tk.END)
            except Exception as e:
                self.append_chat(f"Lỗi gửi: {e}")

    def append_chat(self, msg):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

def main():
    root = tk.Tk()
    app = ChatSender(root)
    root.mainloop()

if __name__ == "__main__":
    main()