import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import *
import datetime
from address import address_list
from parser.parser_chain import *
import openpyxl


# TODO:
# Фикс ошибок с монетами без сетей

def connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet: str) -> object | None:
    try:
        request = requests.get(f"https://pusher.eywa.fi/search?limit=1000&search={wallet}", timeout=10)
        json_data = request.json()
        return json_data
    except requests.exceptions.Timeout as e:
        print("ERROR timeout when connecting to explorer")
        return None


def get_number_of_total_transaction(json_data: object) -> object:
    try:
        total = json_data.get("total", {})
        return total
    except Exception as e:
        print("ERROR when getting number of total transactions")


def get_all_transaction(json_data: object) -> object:
    try:
        all_transaction = json_data.get("result", {})
        return all_transaction
    except Exception as e:
        print("ERROR when getting all transaction")


def get_list_all_transactions_chain(all_transaction: object) -> list:
    try:
        all_transacrions_chain = []
        for i in all_transaction:
            try:
                source = i.get("source", {})
                source_chain_id = source.get("chainId")
                destination = i.get("destination", {})
                destination_chain_id = destination.get("chainId")
                if source_chain_id == "250":
                    tx = source.get("transactionHash")
                    connect = connect_to_ftmscan(tx)
                    info = get_tokens_transfered(connect)
                    sourse_destination = get_token_and_chain_from_info(info)
                    all_transacrions_chain.append(sourse_destination)
                elif destination_chain_id == "250":
                    tx = destination.get("transactionHash")
                    connect = connect_to_ftmscan(tx)
                    info = get_tokens_transfered(connect)
                    sourse_destination = get_token_and_chain_from_info(info)
                    all_transacrions_chain.append(sourse_destination)
                else:
                    source_destination = [source_chain_id, destination_chain_id]
                    all_transacrions_chain.append(source_destination)
            except Exception as e:
                print(f"ERROR {e}")
                continue
        print("----")
        return all_transacrions_chain
    except Exception as e:
        print("Error when get transaction chain")


def build_chain_matrix() -> object:
    try:
        df = pd.DataFrame(0, index=chains_list, columns=chains_list)
        return df
    except Exception as e:
        print("Error when build chain matrix")


def enter_df_from_transaction(df: object, transactions: list) -> object:
    try:
        for pair in transactions:
            if pair == None:
                continue
            df.loc[pair[0], pair[1]] += 1
        return df
    except Exception as e:
        print("Error when enter transaction in df")


def rebuild_df_with_name_of_chain(df: object, chain_list: list) -> object:
    try:
        df.columns = chain_list
        df.index = chain_list
        return df
    except Exception as e:
        print("Error when rebuild matrix")


if __name__ == '__main__':
    while True:
        print("1) Check the total number of transactions by address")
        print("2) Table on transfers from networks to networks by address")
        print("3) Table on transfers from networks to networks by address list")
        print("q) Exit")
        choise = input("-> ")
        if choise == "1":
            wallet = input("Enter wallet address: ")
            req = connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet)
            print(f"Total: {get_number_of_total_transaction(req)}")
        elif choise == "2":
            wallet = input("Enter wallet address: ")
            request = connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet)
            all_transaction = get_all_transaction(request)
            all_chain = get_list_all_transactions_chain(all_transaction)
            df = enter_df_from_transaction(build_chain_matrix(), all_chain)
            # normal_df = rebuild_df_with_name_of_chain(df, chains_list)
            print(df)
            filename = f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
            df.to_excel(filename, sheet_name=wallet[:6])
        elif choise == "3":
            filename = f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
            with pd.ExcelWriter(filename) as writer:
                try:
                    for i in address_list:
                        wallet = i
                        request = connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet)
                        all_transaction = get_all_transaction(request)
                        all_chain = get_list_all_transactions_chain(all_transaction)
                        df = enter_df_from_transaction(build_chain_matrix(), all_chain)
                        normal_df = rebuild_df_with_name_of_chain(df, chains_list)
                        print(normal_df)
                        normal_df.to_excel(writer, sheet_name=wallet[:6])
                except Exception as e:
                    print("Error in 3). Check address_list in address.py")
        elif choise == "q":
            exit()
        else:
            print("There's no such option")
