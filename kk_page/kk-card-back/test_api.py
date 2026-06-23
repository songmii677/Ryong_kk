import requests

url = 'http://127.0.0.1:8000/api/cards/ai-recommend/'

payload = {
    'answers': [
        {
            'key': 'card_type',
            'value': 'credit'
        },
        {
            'key': 'category',
            'value': '음식/카페'
        },
        {
            'key': 'category',
            'value': '음식/카페'
        },
        {
            'key': 'category',
            'value': '쇼핑/간편결제'
        }
    ]
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())