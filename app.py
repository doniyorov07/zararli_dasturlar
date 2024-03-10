import os
from docx import Document
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def count_lines(file_path):
    """Berilgan fayldagi qatorlar sonini hisoblash."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def calculate_directory_stats(directory_path):
    """Direktoriyadagi barcha fayllarning hajmini va qatorlar sonini hisoblash."""
    file_stats = []
    bat_files = []  # .bat fayllarini saqlash uchun ro'yxat

    try:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                size = os.path.getsize(file_path)
                num_lines = 0

                if file_name.endswith('.docx'):
                    doc = Document(file_path)
                    num_lines = len(doc.paragraphs)
                else:
                    num_lines = count_lines(file_path)

                file_stats.append((file_name, size, num_lines))

                # .bat fayllarini tekshirish
                if file_name.endswith('.bat'):
                    bat_files.append(file_name)

            # Katalog ichidagi papkalarni hisoblash
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                subdir_files, subdir_bat_files = calculate_directory_stats(dir_path)
                file_stats.extend(subdir_files)
                bat_files.extend(subdir_bat_files)

    except Exception as e:
        print(f"Xato ro'y berdi: {e}")

    return file_stats, bat_files

def delete_bat_files(directory_path, bat_files):
    """Berilgan papka ichidagi barcha .bat fayllarini o'chirish."""
    try:
        for bat_file in bat_files:
            file_path = os.path.join(directory_path, bat_file)
            os.remove(file_path)
            messagebox.showinfo("O'chirildi", f"{bat_file} fayli o'chirildi.")
    except Exception as e:
        print(f"Xatolik yuzaga keldi: {e}")  # Xatolik haqida ma'lumotni ekranga chiqaramiz
        messagebox.showerror("Xato", f"Fayl o'chirishda xatolik yuz berdi: {e}")

        

def scan_directory(directory_path):
    """Papka tanlanib, skan qilish funksiyasi."""
    # Katalog statistikasini hisoblash
    directory_stats, bat_files = calculate_directory_stats(directory_path)

    if directory_stats:
        # Natijalarni korsatish
        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Papka yo'li: {directory_path}\n")
        for file_name, size, num_lines in directory_stats:
            result_text.insert(tk.END, f"{file_name} - Hajmi: {size} bayt, Qatorlar soni: {num_lines}\n")

        if bat_files:
            # Agar .bat fayllari topsilgan bo'lsa
            result_text.insert(tk.END, "\nViruslar: ")
            for bat_file in bat_files:
                result_text.insert(tk.END, f"{bat_file}, ")

            # O'chirish tugmasi
            delete_button.config(state='normal', command=lambda: delete_bat_files(directory_path, bat_files))
        else:
            result_text.insert(tk.END, "\n.bat fayl topilmadi.")

        result_text.config(state='disabled')
    else:
        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Katalogda fayl topilmadi yoki xatolik yuz berdi.")
        result_text.config(state='disabled')

def choose_directory_and_scan():
    """Foydalanuvchi katalogni tanlash va skan qilish uchun funksiya."""
    directory_path = filedialog.askdirectory()
    if directory_path:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory_path)

def scan_button_clicked():
    """Skan tugmasi bosilganda ishlaydigan funksiya."""
    directory_path = directory_entry.get()
    if directory_path:
        scan_directory(directory_path)

root = tk.Tk()
root.title("Fayl Statistikasi va .bat Faylni O'chirish")

# Papka tanlash uchun tugma
choose_button = tk.Button(root, text="Papka tanlash", command=choose_directory_and_scan)
choose_button.pack(pady=10)

# Papka tanlash tugmasi ichida skan tugmasi
scan_button = tk.Button(root, text="Skaner", command=scan_button_clicked)
scan_button.pack(pady=5)

# Papka yo'lini ko'rsatish uchun so'rov maydoni
directory_entry = tk.Entry(root, width=50)
directory_entry.pack(pady=5)

# Natijalar uchun oyna
result_text = tk.Text(root, height=20, width=50, bg='black', fg='white')
result_text.pack(pady=15)
result_text.config(state='disabled')

# .bat faylni o'chirish tugmasi
delete_button = tk.Button(root, text=".bat faylni o'chirish", state='disabled', command=lambda: delete_bat_files(directory_entry.get(), bat_files))
delete_button.pack(pady=5)

root.mainloop()
