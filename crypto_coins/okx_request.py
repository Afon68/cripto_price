import requests
import json


def okx_request():
    url = "https://www.okx.com/api/v5/market/tickers"
    
    params = {"instType": "SPOT"}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        x = data["data"]
        print(f"✅ len of a response:{len(x)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")