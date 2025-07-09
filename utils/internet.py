# internet.py

import requests

def connected_to_internet(url='http://www.google.com/', timeout=5) -> bool:
    """
    Verifica que haya una conexión a internet activa
    """
    
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

if __name__ == "__main__":
    connected = connected_to_internet()
    print(connected)