import chardet
import json
import sys
import io

# Đặt lại mã hóa đầu ra của stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = 'tiki_products.json'
with open(file_path, 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Mã hóa phát hiện: {encoding}")

# Đọc file với mã hóa phát hiện
raw_data = []
with open(file_path, 'r', encoding=encoding) as file:
    data = json.load(file)
    raw_data = data
# for i in raw_data:
#     print(i)

print(len(raw_data))
