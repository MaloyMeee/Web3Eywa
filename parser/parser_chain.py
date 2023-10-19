import requests
from bs4 import BeautifulSoup
import re


def connect_to_ftmscan(tx: str) -> object | None:
    try:
        request = requests.get(f"https://ftmscan.com/tx/{tx}", timeout=10,
                               headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        return request
    except requests.exceptions.Timeout as e:
        print("ERROR timeout when connecting to ftmscan")
        return None


def get_tokens_transfered(request: object, tx) -> list | None:
    try:
        soup = BeautifulSoup(request.text, "lxml")
        li = soup.find_all("li", class_="media align-items-baseline mb-2")
        first_li = li[0]
        first_li_div = first_li.find("div", class_="media-body")
        first_info = first_li_div.find_all("a")[2].text
        last_li = li[len(li) - 1]
        last_li_div = last_li.find("div", class_="media-body")
        last_info = last_li_div.find_all("a")[2].text
        amount = last_li_div.find_all("span", class_="mr-1")[3].text
        info = [first_info, last_info, amount]
        return info
    except IndexError:
        li = soup.find_all("li", class_="media align-items-baseline mb-0")
        first_li = li[0]
        first_li_div = first_li.find("div", class_="media-body")
        first_info = first_li_div.find_all("a")[2].text
        amount = first_li_div.find_all("span", class_="mr-1")[3].text
        if first_info == "EUSD (EUSD) ":
            return ["EUSD (EUSD) ", "EUSD (EUSD) ", amount]
        else:
            pattern = re.search(r"s(\w+)\W*\w?_(\w+)", first_info)[2]
            return [f"sUSDT_{pattern}", f"sUSDT_{pattern}", amount]

    except Exception as e:
        print(f"ERROR in getting information about chains {e} | {tx}")
        return None


def get_token_and_chain_from_info(info: list) -> list | None:
    try:
        source_chain = re.search(r"s(\w+)\W*\w?_(\w+)", info[0])[2]
        destination_chain = re.search(r"s(\w+)\W*\w?_(\w+)", info[1])[2]
        chain = [source_chain, destination_chain, info[2]]
        return chain
    except Exception as e:
        try:
            if info[0] == 'EUSD (EUSD) ' and info[1] == 'EUSD (EUSD) ':
                destination_chain = "FTM"
                source_chain = "FTM"
                chain = [source_chain, destination_chain, info[2]]
                return chain
            try:
                if info[0] == 'EUSD (EUSD) ' or re.search(r'(Curve)', info[0])[1] != None:
                    source_chain = "FTM"
                    destination_chain = re.search(r"s(\w+)\W*\w?_(\w+)", info[1])[2]
                    chain = [source_chain, destination_chain, info[2]]
                    return chain
            except Exception as e:
                try:
                    if info[1] == 'EUSD (EUSD) ' or re.search(r'(Curve)', info[1])[1] != None:
                        destination_chain = "FTM"
                        source_chain = re.search(r"s(\w+)\W*\w?_(\w+)", info[0])[2]
                        chain = [source_chain, destination_chain, info[2]]
                        return chain
                except Exception as e:
                    print(f"ERROR 1 {info} {e}")
                    return None
        except Exception as e:
            print(f"ERROR 2 {info} {e} |")
        print(f"ERROR 3 {info} {e}")
        return None
