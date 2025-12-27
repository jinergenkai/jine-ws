import requests

def extract_text_from_image(image_path: str, api_url: str = "http://localhost:8000/extract"):
    """
    Example client to use the Vintern OCR API

    Parameters:
    - image_path: Path to the image file
    - api_url: URL of the API endpoint
    """
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(api_url, files=files)

    if response.status_code == 200:
        result = response.json()
        print(f"Question: {result['question']}")
        print(f"\nExtracted Text:\n{result['text']}")
        return result
    else:
        print(f"Error: {response.status_code}")
        try:
            print(response.json())
        except:
            print("Response text:", response.text)
        return None

def extract_with_custom_question(image_path: str, question: str, api_url: str = "http://localhost:8000/extract"):
    """
    Extract text with a custom question

    Parameters:
    - image_path: Path to the image file
    - question: Custom question to ask about the image
    - api_url: URL of the API endpoint
    """
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'question': question}
        response = requests.post(api_url, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        print(f"Question: {result['question']}")
        print(f"\nExtracted Text:\n{result['text']}")
        return result
    else:
        print(f"Error: {response.status_code}")
        try:
            print(response.json())
        except:
            print("Response text:", response.text)
        return None

def extract_full_text(image_path: str, max_num: int = 12, max_new_tokens: int = 4096, api_url: str = "http://localhost:8000/extract"):
    """
    Extract full text from image with lots of text

    Parameters:
    - image_path: Path to the image file
    - max_num: Maximum number of image blocks (higher = more detail, slower)
    - max_new_tokens: Maximum output length (higher = more text extracted)
    - api_url: URL of the API endpoint
    """
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {
            'max_num': str(max_num),
            'max_new_tokens': str(max_new_tokens)
        }
        response = requests.post(api_url, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        print(f"Question: {result['question']}")
        print(f"\nExtracted Text:\n{result['text']}")
        print(f"\nText length: {len(result['text'])} characters")
        return result
    else:
        print(f"Error: {response.status_code}")
        try:
            print(response.json())
        except:
            print("Response text:", response.text)
        return None

if __name__ == "__main__":
    # Basic extraction
    result = extract_text_from_image('Red_Apple.jpg')

    # For images with LOTS of text, use higher limits:
    # result = extract_full_text('document.jpg', max_num=12, max_new_tokens=8192)

    # Custom question
    # result = extract_with_custom_question(
    #     'test-image.jpg',
    #     'Mô tả chi tiết nội dung trong ảnh này.'
    # )
