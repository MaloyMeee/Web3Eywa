import requests
from bs4 import BeautifulSoup



def connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet: str):
    try:
        request = requests.get(f"https://pusher.eywa.fi/search?offset=20&limit=20&search={wallet}", timeout=10)
        json_data = request.json()
        return json_data
    except requests.exceptions.Timeout as e:
        print("ERROR timeout when connecting to explorer")

def get_number_of_total_transaction(json_data):
    total = json_data.get("total", {})
    return total


if __name__ == '__main__':
    while True:
        print("\n")
        print("1) Check number of transactions")
        print("q) Exit")
        choise = input("-> ")
        if choise == "1":
            wallet = input("Enter wallet address: ")
            req = connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet)
            print(get_number_of_total_transaction(req))
        elif choise == "q":
            exit()
        else:
            print("There's no such option")