import requests
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

try:
    all_data = []
    for page in range(1, 3):  
        api_url = f"https://tiki.vn/api/personalish/v1/blocks/listings?limit=20&aggregations=2&version=home-persionalized&trackity_id=4471f252-df28-9379-7e47-68a9e4baef6c&category=1520&page={page}&urlKey=lam-dep-suc-khoe"
        # api_url = f"https://tiki.vn/api/v2/products?limit=20&sort=top_seller&q=m%C4%A9+ph%E1%BA%A9m&page={page}"
        # api_url = f"https://tiki.vn/api/v2/products?limit=40&sort=top_seller&q=m%C5%A9+b%E1%BA%A3o+hi%E1%BB%83m&page={page}"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        all_data.extend(data["data"])  
        time.sleep(1)  # 

    with open("tiki_products.json", "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

    print("Dữ liệu đã được lưu thành công vào tiki_products.json")
except requests.exceptions.RequestException as e:
    print(f"Lỗi khi gửi yêu cầu tới API: {e}")

