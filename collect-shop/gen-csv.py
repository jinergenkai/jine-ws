from dataclasses import dataclass
from typing import List, Optional

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
# get data from tiki_products



@dataclass
class Badge:
    type: str
    code: str
    text: Optional[str] = None
    icon: Optional[str] = None


@dataclass
class Product:
    id: int
    sku: str
    name: str
    seller_name: str
    brand_name: str
    price: float
    original_price: float
    discount: float
    discount_rate: int
    rating_average: float
    review_count: int
    thumbnail_url: str
    quantity_sold: int
    category_name: str
    # badges: List[Badge]


# Ví dụ ánh xạ JSON vào class
json_data = raw_data

# Chuyển JSON sang object
def parse_product(data: dict) -> Product:
    # badges = [Badge(**badge) for badge in data.get("badges_new", [])]
    return Product(
        id=data.get("id", ""),
        sku=data.get("sku", ""),
        name=data.get("name", ""),
        seller_name=data.get("seller_name", ""),
        brand_name=data.get("brand_name", ""),
        price=data.get("price", 0.0),
        original_price=data.get("original_price", 0.0),
        discount=data.get("discount", 0.0),
        discount_rate=data.get("discount_rate", 0.0),
        rating_average=data.get("rating_average", 0.0),
        review_count=data.get("review_count", 0),
        thumbnail_url=data.get("thumbnail_url", ""),
        quantity_sold=data.get("quantity_sold", {}).get("value", 0),  # Xử lý giá trị null cho quantity_sold
        category_name=data.get("primary_category_name", ""),
    )


product = []

for item in json_data:
    product.append(parse_product(item))

# In object
print(len(product))




# export to excel
import re
import pandas as pd
import xlsxwriter

# Hàm để loại bỏ các ký tự không hợp lệ trong tên
def clean_string(s: str) -> str:
    # Thay thế bất kỳ ký tự không hợp lệ nào bằng chuỗi rỗng
    # Ký tự hợp lệ trong Excel là từ 0x20 đến 0x7F trong bảng mã ASCII
    return re.sub(r'[^\x20-\x7E]', '', s)

# Giả sử bạn đã có object product đã được điền dữ liệu
# product = [Product1, Product2, ..., ProductN]

# Làm sạch dữ liệu trong product
# for product_item in product:
#     product_item.name = clean_string(product_item.name)  # Làm sạch tên sản phẩm

# Chuyển product thành DataFrame
product_df = pd.DataFrame([product_item.__dict__ for product_item in product])





import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl import Workbook


# Tạo một file Excel mới sử dụng xlsxwriter
with pd.ExcelWriter('products.xlsx', engine='xlsxwriter') as writer:
    # Ghi dữ liệu vào worksheet
    product_df.to_excel(writer, index=False, sheet_name='Products')

    # Lấy workbook và worksheet từ ExcelWriter
    workbook  = writer.book
    worksheet = writer.sheets['Products']

    # Lấy số dòng và số cột của dữ liệu
    num_rows, num_cols = product_df.shape

    # Tạo một bảng (table) với dữ liệu trong worksheet
    worksheet.add_table(0, 0, num_rows, num_cols - 1, {'columns': [{'header': col} for col in product_df.columns]})

    # Áp dụng một số định dạng cho bảng
    worksheet.set_column('A:Z', 20)  # Căn chỉnh độ rộng cột
    worksheet.set_row(0, None, None, {'bold': True, 'bg_color': '#4F81BD', 'font_color': 'white'})  # Định dạng tiêu đề

    # Đảm bảo rằng không có ký tự không hợp lệ trong chuỗi Unicode
    for row_num in range(num_rows):
        for col_num in range(num_cols):
            cell_value = product_df.iloc[row_num, col_num]
            if isinstance(cell_value, str):
                worksheet.write_string(row_num + 1, col_num, cell_value)  # Ghi chuỗi Unicode
            else:
                worksheet.write(row_num + 1, col_num, cell_value)  # Ghi giá trị không phải chuỗi

print("File Excel đã được tạo thành công!")
