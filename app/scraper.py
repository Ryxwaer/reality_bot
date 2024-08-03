import requests
from typing import List, Any


def fetch_new_listings(url: str) -> List[dict]:
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []
