import requests
from config import *
from bs4 import BeautifulSoup
import lxml
import re


def connect_to_ftmscan(tx: str) -> object | None:
    try:
        request = requests.get(f"https://ftmscan.com/tx/{tx}", timeout=10,
                               headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        return request
    except requests.exceptions.Timeout as e:
        print("ERROR timeout when connecting to ftmscan")
        return None


def get_tokens_transfered(request: object) -> list | None:
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
    except Exception as e:
        print(f"ERROR in getting information about chains {e}")
        return None


def get_token_and_chain_from_info(info: list) -> list | None:
    try:
        source_chain = re.search(r"s(\w+)\W*\w?_(\w+)", info[0])[2]
        destination_chain = re.search(r"s(\w+)\W*\w?_(\w+)", info[1])[2]
        chain = [source_chain, destination_chain]
        return chain
    except Exception as e:
        print(f"ERROR in regular find {info}")
        return None

# conn = connect_to_ftmscan("0x1c8a2d27aa45ba4cac628363ba5557ffe3510f04bf07c21463de0fb75954ecb2")
# infoo = get_tokens_transfered(conn)
# get_token_and_chain_from_info(infoo)
