import requests
from config import *
import pandas as pd
import re


def get_address_list_from_file() -> list[str]:
    """
    Получение списков адресов из файла
    """
    address_file = open("address.txt", "r")
    address_list = address_file.readlines()
    clear_address_list = []
    for sub in address_list:
        clear_address_list.append(re.sub('\n', '', sub))
    address_file.close()
    return clear_address_list


def connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet: str) -> object:
    """
    Запрос на Eywa Explorer, получение json объекта
    """
    try:
        request = requests.get(f"https://pusher.eywa.fi/search?limit=10000&search={wallet}", timeout=10)
        json_data = request.json()
        return json_data
    except requests.exceptions.Timeout:
        print("ERROR timeout when connecting to explorer")
        return None


def get_number_of_total_transaction(json_data: object) -> object:
    """
    Получение из json объекта количество всех транзакций по кошельку
    """
    try:
        total = json_data.get("total", {})
        return total
    except Exception:
        print("ERROR when getting number of total transactions")


def get_all_transactions(json_data: object) -> list[dict]:
    """
    Получение списка транзакций
    """
    try:
        all_transaction = json_data.get("result", {})
        return all_transaction
    except Exception:
        print("ERROR when getting all transaction")


def search_amount(source, destination):
    events = source.get("events")
    if source.get("events") is not None:
        for i in range(0, len(events) - 1):
            if len(source.get("events")[i].get("args", {})) != 0:
                if len(source.get("events")[i].get("args", {}).get("_value")) != 0:
                    if source.get("events")[i].get("args", {}).get("_value") != "0":
                        return source.get("events")[i].get("args", {}).get("_value")
                    else:
                        continue
                else:
                    continue
            else:
                continue
    else:
        events = destination.get("events")
        for i in range(1, len(events)):
            if destination.get("events")[len(events) - i] is not None:
                if len(destination.get("events")[len(events) - i].get("args", {})) != 0:
                    if len(destination.get("events")[len(events) - i].get("args", {}).get("amount", {})) != 0:
                        return destination.get("events")[len(events) - i].get("args", {}).get("amount", {})
                    else:
                        continue
                else:
                    continue
            else:
                continue


# TODO:
# Узнать что такое [chain,chain] и [chain, 0]
def get_chainlist_and_amount_in_all_transaction(all_transaction: list[dict]) -> list[list]:
    """
    Получение списка  входящих и исходящих сетей, а также сумму по каждой транзакции. Вид [source, destination, amount]
    """
    chains_list_and_amount_in_all_transaction = []
    for transaction in all_transaction:
        source = transaction.get("source", {})
        source_chain = source.get("chainId", {})
        destination = transaction.get("destination", {})
        destination_chain = destination.get("chainId", {})
        if source_chain == "250":
            events = source.get("events")
            source_chain = events[len(events) - 1].get("args", {}).get("nextChainId")
            if source_chain is None:
                source_chain = events[len(events) - 2].get("args", {}).get("nextChainId")
        elif destination_chain == "250":
            events = destination.get("events")
            destination_chain = events[len(events) - 1].get("args", {}).get("nextChainId")
            if destination_chain is None:
                destination_chain = events[len(events) - 2].get("args", {}).get("nextChainId")
        amount = search_amount(source, destination)
        tx = transaction.get("requestId")
        chains_list_and_amount_in_all_transaction.append([source_chain, destination_chain, amount, tx])
    return chains_list_and_amount_in_all_transaction


def build_chain_matrix() -> object:
    """
    Построение таблицы сетей
    """
    df = pd.DataFrame(0, index=chains_list_rev, columns=chains_list_rev)
    return df


def rebuild_df_with_name_of_chain(df: object) -> object:
    """
    Перестроение мартицы под лицеприятный вид с заголовками в виде названий сетей а не цифр
    """
    df.columns = chains_list
    df.index = chains_list
    return df


def enter_df_from_transaction(df: object, transactions: list) -> float | object:
    """
    Заполнение таблицы использования чейнов
    """
    amount = 0
    # max_amount = 0
    total_transactions = 0
    for pair in transactions:
        if pair[0] is None:
            continue
        if pair[1] is None:
            continue
        if pair[0] == "0":
            continue
        if pair[1] == "0":
            continue
        if pair[0] == "1313161554":
            continue
        if pair[1] == "1313161554":
            continue
        df.loc[int(pair[0]), int(pair[1])] += 1
        amount += convert_amount(pair[2])
        total_transactions += 1
        # if convert_amount(pair[2]) > max_amount:
        #     max_amount = convert_amount(pair[2])
        #     tx = pair[3]
    return df, amount, total_transactions


def convert_amount(amount: str) -> float:
    """
    Конвертация суммы без разделителя в нормальный вид
    """
    if len(amount) <= 14:
        amount_list = list(amount)
        amount_list.insert(len(amount_list) - 6, ".")
        string = "".join(amount_list)
        return float(string)
    elif len(amount) >= 19:
        amount_list = list(amount)
        amount_list.insert(len(amount_list) - 18, ".")
        string = "".join(amount_list)
        return float(string)
    else:
        return float(1)
