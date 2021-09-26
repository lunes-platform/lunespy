from lunespy.utils.settings import bcolors


def log_transaction(data: dict) -> None:
    func = lambda tuple: print(f"{tuple[0]}\n {bcolors.OKGREEN + '└── ' + str(tuple[1])  + bcolors.ENDC}")
    list(map(func, data.items()))


def save_transaction(data: dict) -> None:
    import json

    with open(f"./transaction-{data['response']['id']}.json", 'w') as file:
        file.write(json.dumps(data['response']))

    print(f"\n{bcolors.OKCYAN}Your Transaction has been sended and saved in `./transaction-{data['response']['id']}.json`{bcolors.ENDC}")