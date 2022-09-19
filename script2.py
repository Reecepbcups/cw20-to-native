'''
Loops over all JSON files in CW20s folder, then converts out the actual balances
'''

import os
import json
import base64

from dotenv import load_dotenv
load_dotenv()

TOKEN_FACTORY_DENOM = os.getenv("TOKEN_FACTORY_DENOM", "factory/addr/denom")
WALLET_PREFIX = os.getenv("WALLET_PREFIX", "juno")
EVED_NODE = os.getenv("EVED_NODE", "http://localhost:26657")

current_dir = os.path.dirname(os.path.realpath(__file__))
CW20s = os.path.join(current_dir, 'CW20s')

def hex_string_to_uft8(hex_string):
    return bytearray.fromhex(hex_string).decode()

def base64_to_uft8(base64_string):
    return base64.b64decode(base64_string).decode()

balances = {}
total_balances = 0

for file in os.listdir(CW20s):
    # read the file
    with open(os.path.join(CW20s, file), 'r') as f:
        data = json.load(f)

        # get models key if found
        if 'models' not in data:
            continue

        modules = list(data['models'])

        for m in modules:
            key = hex_string_to_uft8(m['key'])
            if 'balance' not in key:
                break
            
            # TODO: clean this mess up yuck
            # remove balance from the string
            address = str(key.replace('balance', '')) # balancejuno1000xz25ydz8h9rwgnv30l9p0x500dvj0s9yyc9 -> juno1000xz25ydz8h9rwgnv30l9p0x500dvj0s9yyc9
            address = WALLET_PREFIX + key.split(WALLET_PREFIX)[1]
            balance = int(base64_to_uft8(m['value']).replace('"', '')) # TODO: try catch

            # print(f'{address} - {balance}')
            if balance <= 0:
                continue

            balances[address] = balance
            total_balances += balance

# save balances to a file as JSON
with open(os.path.join(current_dir, 'balances.json'), 'w') as f:
    json.dump(balances, f)
    print("Balances saved to balances.json. Total Value: {total_balances:.0f}")

# loop through balances
output = []
for address, balance in balances.items():    
    output.append(f"eved tx tokenfactory mint-and-send-tokens {TOKEN_FACTORY_DENOM} {balance} {address} --node {EVED_NODE}")

# save to file
script='factory_mint.sh'
with open(os.path.join(current_dir, script), 'w') as f:
    f.write('\n'.join(output))
    print(f"Token Factory commands saved to {script}")