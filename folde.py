from google.colab import drive
import os
import shutil

drive.mount('/content/drive')

src_folder = "/content/drive/MyDrive/folder_name"
dst_folder = "/content/drive/MyDrive/folder_name (Backup Copy)"
ignore_ext = (".gdoc", ".gsheet", ".gslides")

def get_folder_stats(path, ignore_ext=()):
    total_size = 0
    total_files = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if not any(f.endswith(ext) for ext in ignore_ext):
                try:
                    total_size += os.path.getsize(full_path)
                    total_files += 1
                except:
                    pass
    return total_size, total_files

def smart_copytree(src, dst, ignore_ext=()):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if any(s.endswith(ext) for ext in ignore_ext):
            continue

        if os.path.isdir(s):
            smart_copytree(s, d, ignore_ext)
        else:
            if not os.path.exists(d) or os.path.getsize(s) != os.path.getsize(d):
                shutil.copy2(s, d)

print("جاري نسخ الملفات الجديدة فقط...")
smart_copytree(src_folder, dst_folder, ignore_ext)
print("النسخ انتهى.")

src_size, src_count = get_folder_stats(src_folder, ignore_ext)
dst_size, dst_count = get_folder_stats(dst_folder, ignore_ext)

print("إحصائيات التحقق:")
print(f"المصدر: {src_count} ملف / {round(src_size / (1024*1024), 2)} MB")
print(f"النسخة: {dst_count} ملف / {round(dst_size / (1024*1024), 2)} MB")

if src_size == dst_size and src_count == dst_count:
    print("التحقق ناجح: النسخة مطابقة تماماً")
else:
    print("تحذير: يوجد فرق بين الأصل والنسخة! تحقق يدويًا من الملفات.")
