import tkinter as tk
from tkinter import scrolledtext
from client import Client
import threading

class AESRSAChatUI:
    def __init__(self, master):
        self.master = master
        self.master.title('AES-RSA Socket Chat')
        self.client = Client()

        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=70, height=20)
        self.text_area.grid(row=0, column=0, columnspan=2, padx=8, pady=8)

        self.entry = tk.Entry(master, width=60)
        self.entry.grid(row=1, column=0, padx=8, pady=8)

        self.send_btn = tk.Button(master, text='Send', command=self.send_message)
        self.send_btn.grid(row=1, column=1, padx=8, pady=8)

        self.connect_btn = tk.Button(master, text='Connect', command=self.connect)
        self.connect_btn.grid(row=2, column=0, sticky='w', padx=8)

        self.status_label = tk.Label(master, text='Disconnected')
        self.status_label.grid(row=2, column=1, sticky='e', padx=8)

    def connect(self):
        if self.client.connect():
            self.status_label.config(text='Connected')
            self.log('Connected to server')
            threading.Thread(target=self.client.receive_messages, daemon=True).start()
        else:
            self.log('Connection failed')

    def send_message(self):
        msg = self.entry.get().strip()
        if msg:
            self.client.send_message(msg)
            self.entry.delete(0, tk.END)

    def log(self, text):
        self.text_area['state'] = 'normal'
        self.text_area.insert(tk.END, text + '\n')
        self.text_area.yview(tk.END)
        self.text_area['state'] = 'disabled'

if __name__ == '__main__':
    root = tk.Tk()
    app = AESRSAChatUI(root)
    root.mainloop()
