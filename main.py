from logic import *

print("""
░██╗░░░░░░░██╗███████╗██████╗░██████╗░███████╗██╗░░░██╗░██╗░░░░░░░██╗░█████╗░
░██║░░██╗░░██║██╔════╝██╔══██╗╚════██╗██╔════╝╚██╗░██╔╝░██║░░██╗░░██║██╔══██╗
░╚██╗████╗██╔╝█████╗░░██████╦╝░█████╔╝█████╗░░░╚████╔╝░░╚██╗████╗██╔╝███████║
░░████╔═████║░██╔══╝░░██╔══██╗░╚═══██╗██╔══╝░░░░╚██╔╝░░░░████╔═████║░██╔══██║
░░╚██╔╝░╚██╔╝░███████╗██████╦╝██████╔╝███████╗░░░██║░░░░░╚██╔╝░╚██╔╝░██║░░██║By
░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═════╝░╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝  [G7]AzaZLO""")


def check_total_number_of_transaction_by_address(wallet: str) -> None:
    json_data = connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet)
    print(f"Total number of transaction:{get_number_of_total_transaction(json_data)}")


def table_on_transfers_from_networks_to_networks_by_adrress() -> None:
    wallet = input("Enter wallet address: ")
    json_data = connect_to_eywa_explorer_and_get_transaction_per_wallet(wallet)
    all_transaction = get_all_transactions(json_data)
    x = get_chainlist_and_amount_in_all_transaction(all_transaction)
    df = build_chain_matrix()
    dff, amount, total_transactions = enter_df_from_transaction(df, x)
    print(rebuild_df_with_name_of_chain(df))
    print(f"Total number of transactions: {total_transactions}")
    print(f"Total volume: {amount}")


def table_on_transfers_from_networks_to_networks_by_adrress_list() -> None:
    for i in get_address_list_from_file():
        json_data = connect_to_eywa_explorer_and_get_transaction_per_wallet(i)
        all_transaction = get_all_transactions(json_data)
        x = get_chainlist_and_amount_in_all_transaction(all_transaction)
        df = build_chain_matrix()
        dff, amount, total_transactions = enter_df_from_transaction(df, x)
        print(rebuild_df_with_name_of_chain(df))
        print(f"Total number of transactions: {total_transactions}")
        print(f"Total volume: {amount}")


if __name__ == '__main__':
    while True:
        print("1) Check the number of transactions, taking into account service transactions, by burn type")
        print("2) Table on transfers from networks to networks by address")
        print("3) Table on transfers from networks to networks by address list")
        print("q) Exit")
        choise = input("-> ")
        if choise == "1":
            wallet = input("Enter wallet address: ")
            check_total_number_of_transaction_by_address(wallet)
        elif choise == "2":
            table_on_transfers_from_networks_to_networks_by_adrress()
        elif choise == "3":
            table_on_transfers_from_networks_to_networks_by_adrress_list()
        elif choise == "q":
            exit()
        else:
            print("There's no such option")
