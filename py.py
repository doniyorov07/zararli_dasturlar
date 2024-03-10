import os
from docx import Document

def count_lines(file_path):
    """Berilgan fayldagi qatorlar sonini hisoblash."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def calculate_directory_stats(directory_path):
    """Direktoriyadagi barcha fayllarning hajmini va qatorlar sonini hisoblash."""
    file_stats = []
    try:
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                num_lines = 0

                # Docx fayllari uchun
                if file_name.endswith('.docx'):
                    doc = Document(file_path)
                    num_lines = len(doc.paragraphs)
                else:
                    num_lines = count_lines(file_path)  # Boshqa formatdagi fayllar uchun

                file_stats.append((file_name, size, num_lines))
    except Exception as e:
        print(f"Xato ro'y berdi: {e}")
    return file_stats

def main():
    directory_path = input("Izlashni boshlash uchun direktoriya yo'lini kiriting: ")
    directory_stats = calculate_directory_stats(directory_path)

    if directory_stats:
        print(f"Papka yo'li: {directory_path}")
        for file_name, size, num_lines in directory_stats:
            print(f"{file_name} - Hajmi: {size} bayt, Qatorlar soni: {num_lines}")
    else:
        print("Katalogda fayl topilmadi yoki xatolik yuz berdi.")

if __name__ == "__main__":
    main()
