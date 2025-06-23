from dataclasses import dataclass
from typing import Optional, List



import chardet
import json
import sys
import io

# Đặt lại mã hóa đầu ra của stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = 'shope_products.json'
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
class Product:
    itemid: int
    shopid: int
    name: str
    # image: str
    # currency: str
    stock: int
    status: int
    sold: int
    historical_sold: int
    liked_count: int
    # catid: int
    brand: Optional[str]
    price: float
    price_before_discount: float
    discount: Optional[str]
    rating_star: float
    rating_count: List[int]
    review_count_with_context: int
    review_count_with_image: int
    # add_on_deal_id: Optional[int]
    # add_on_deal_label: Optional[str]
    # is_preferred_plus_seller: bool
    shop_location: Optional[str]
    voucher_code: Optional[str]
    voucher_label: Optional[str]
    shop_name: Optional[str]
    display_sold_count: int

# Hàm chuyển đổi JSON sang đối tượng `Product`
def parse_product(data: dict) -> Product:
    item_basic = data.get("item_basic", {}) or {}
    item_rating = item_basic.get("item_rating", {}) or {}
    add_on_deal_info = item_basic.get("add_on_deal_info", {}) or {}
    voucher_info = item_basic.get("voucher_info", {}) or {}

    return Product(
        itemid=item_basic.get("itemid", 0),
        shopid=item_basic.get("shopid", 0),
        name=item_basic.get("name", ""),
        # image=item_basic.get("image", ""),
        # currency=item_basic.get("currency", ""),
        stock=item_basic.get("stock", 0),
        status=item_basic.get("status", 0),
        sold=item_basic.get("sold", 0),
        historical_sold=item_basic.get("historical_sold", 0),
        liked_count=item_basic.get("liked_count", 0),
        # catid=item_basic.get("catid", 0),
        brand=item_basic.get("brand", ""),
        price=item_basic.get("price", 0.0) / 100000,  # Giá trị gốc chia 100000 để chuyển đổi sang VND
        price_before_discount=item_basic.get("price_before_discount", 0.0) / 100000,
        discount=item_basic.get("discount", ""),
        rating_star=item_rating.get("rating_star", 0.0),
        rating_count=item_rating.get("rating_count", []),
        review_count_with_context=item_rating.get("rcount_with_context", 0),
        review_count_with_image=item_rating.get("rcount_with_image", 0),
        # add_on_deal_id=add_on_deal_info.get("add_on_deal_id", ""),
        # add_on_deal_label=add_on_deal_info.get("add_on_deal_label", ""),
        # is_preferred_plus_seller=item_basic.get("is_preferred_plus_seller", False),
        shop_location=item_basic.get("shop_location", ""),
        voucher_code=voucher_info.get("voucher_code", ""),
        voucher_label=voucher_info.get("label", ""),
        shop_name=item_basic.get("shop_name", ""),
        display_sold_count=item_basic.get("item_card_display_sold_count", {}).get("display_sold_count", 0),
    )


# Ví dụ sử dụng
import json

json_data = raw_data

product = []

for item in json_data:
    product.append(parse_product(item))

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


# Hàm chuyển đổi từ MacRoman sang UTF-8
def macroman_to_utf8(value):
    if isinstance(value, str):  # Chỉ xử lý chuỗi
        try:
            # Chuyển đổi từ MacRoman sang UTF-8
            return value.encode('mac_roman').decode('utf-8')
        except UnicodeDecodeError:
            # Nếu không chuyển đổi được, trả về giá trị gốc
            return value
    return value  # Giá trị không phải chuỗi giữ nguyên

# Áp dụng chuyển đổi cho toàn bộ DataFrame
product_df = product_df.applymap(macroman_to_utf8)




import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl import Workbook


# Tạo một file Excel mới sử dụng xlsxwriter
with pd.ExcelWriter('shope_products.xlsx', engine='xlsxwriter') as writer:
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
        if isinstance(cell_value, str):  # Nếu là chuỗi
            worksheet.write_string(row_num + 1, col_num, cell_value)
        elif isinstance(cell_value, list):  # Nếu là danh sách
            # Chuyển danh sách thành chuỗi, nối bằng dấu phẩy
            worksheet.write_string(row_num + 1, col_num, ", ".join(map(str, cell_value)))
        else:  # Các giá trị khác (số, None, v.v.)
            worksheet.write(row_num + 1, col_num, cell_value)
print("File Excel đã được tạo thành công!")
