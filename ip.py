import nmap
import tkinter as tk
from tkinter import ttk
import socket
import requests 
import uuid  # mac olish uchun
from tkinter import filedialog

# API key
API_KEY = "235803B20FD4AEDA6293E28F73F5E4BB"

class NetworkScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("Portni tekshirish")
        master.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        # IP manzili uchun maydon
        self.ip_label = tk.Label(self.master, text="IP manzilini kiriting:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.pack()

        # Port oralig'ini kiritish uchun maydon
        self.port_range_label = tk.Label(self.master, text="Port oralig'ini kiriting (masalan, 20-100):")
        self.port_range_label.pack()

        self.port_range_entry = tk.Entry(self.master)
        self.port_range_entry.pack()

        # Portlarni tekshirish tugmasi
        self.check_button = tk.Button(self.master, text="Portlarni tekshirish", command=self.check_ports)
        self.check_button.pack()

        # Natija jadvali
        self.result_table = ttk.Treeview(self.master, columns=("Attribute", "Value"))
        self.result_table.heading("#1", text="Attribute")
        self.result_table.heading("#2", text="Value")
        self.result_table.pack()

        # Export tugmasi
        self.export_button = tk.Button(self.master, text="Export", command=self.export_data)
        self.export_button.pack()

        # Ma'lumotlar uchun label
        self.result_label = tk.Label(self.master, text="", wraplength=400)
        self.result_label.pack()

    def check_ip(self, ip_address):
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False

    def get_ip_info(self, ip_address):
        try:
            url = f"https://api.ip2location.io/?key={API_KEY}&ip={ip_address}"
            response = requests.get(url)
            data = response.json()
            return data
        except Exception as e:
            print(f"Error: {e}")
        return None

    def is_local_ip(self, ip_address):
        # Lokal IP manzillari
        local_ip_prefixes = ['172.', '192.']
        for prefix in local_ip_prefixes:
            if ip_address.startswith(prefix):
                return True
        return False

    def get_local_ip_info(self, ip_address):
        if self.is_local_ip(ip_address):
            return self.get_ip_info(ip_address)
        else:
            return None

    def check_ports(self):
        ip_address = self.ip_entry.get()
        port_range = self.port_range_entry.get()  # Port oralig'i

        if ip_address:
            if not self.check_ip(ip_address):
                self.result_label.config(text=f"{ip_address} - bu to'g'ri IP manzil emas!", fg="red")
                self.export_button.config(state="disabled")  # Ma'lumotlar topilmadi, exportni o'chirish
                return

            try:
                open_ports = []
                closed_ports = []

                # Yangi portlar uchun tekshiruv qismi
                start_port, end_port = map(int, port_range.split('-'))
                for port in range(start_port, end_port + 1):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result_port = sock.connect_ex((ip_address, port))
                    sock.close()

                    if result_port == 0:
                        open_ports.append(port)
                    else:
                        closed_ports.append(port)

                # Jadvalni tayyorlash
                self.result_table.delete(*self.result_table.get_children())
                for port in open_ports:
                    self.result_table.insert("", tk.END, values=(port, "Ochiq"))
                for port in closed_ports:
                    self.result_table.insert("", tk.END, values=(port, "Yopiq"))

                # Ma'lumotlarni chiqarish
                ip_info = self.get_local_ip_info(ip_address)

                if ip_info:
                    for key, value in ip_info.items():
                        self.result_table.insert("", tk.END, values=(key, value))
                    self.export_button.config(state="normal")  # Ma'lumotlar topildi, exportni aktivlashtirish
                else:
                    ip_info_global = self.get_ip_info(ip_address)
                    if ip_info_global:
                        for key, value in ip_info_global.items():
                            self.result_table.insert("", tk.END, values=(key, value))
                        self.export_button.config(state="normal")  # Ma'lumotlar topildi, exportni aktivlashtirish
                    else:
                        self.result_label.config(text="Ma'lumotlar topilmadi", fg="green")
                        self.export_button.config(state="disabled")  # Ma'lumotlar topilmadi, exportni o'chirish

            except Exception as e:
                self.result_label.config(text=str(e), fg="red")
                self.export_button.config(state="disabled")  # Xatolik sodir bo'lganda, exportni o'chirish
        else:
            self.result_label.config(text="Iltimos, IP manzilini kiriting!", fg="red")
            self.export_button.config(state="disabled")  # IP manzil kiritilmagan, exportni o'chirish

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    for child in self.result_table.get_children():
                        attribute, value = self.result_table.item(child, "values")
                        file.write(f"{attribute}: {value}\n")
                self.result_label.config(text="Ma'lumotlar faylga yozildi", fg="blue")
            except Exception as e:
                self.result_label.config(text=f"Xato: {e}", fg="red")
        else:
            self.result_label.config(text="Faylni saqlash bekor qilindi", fg="red")

root = tk.Tk()
app = NetworkScannerApp(root)
root.mainloop()


