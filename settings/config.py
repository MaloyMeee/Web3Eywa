chains_dic = {"FTM": 250,
              "ETH": 1,
              "POL": 137,
              "BSC": 56,
              "AVAX": 43114,
              "ARB": 42161,
              "OP": 10}
chains_dic_rev = {250: "Fantom",
                  1: "Ethereum",
                  137: "Polygon",
                  56: "BSC",
                  43114: "Avalanche",
                  42161: "Arbitrum",
                  10: "Optimism"}

chains_list = list(chains_dic.keys())
chains_list_rev = list(chains_dic_rev.keys())
NUMBER_OF_CHAIN = len(chains_dic)
FTMSCAN="https://ftmscan.com/tx/"