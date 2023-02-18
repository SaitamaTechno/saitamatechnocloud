#pip3 install block-io

from block_io import BlockIo

version = 2
dogee = BlockIo('17ec-ba4d-9a1b-8226', 'bitemyass1907eatmyshit1907', version) #for dogeecoin

def create_new_wallet(name):
    dogee.get_new_address(label=name)

def get_wallet_info(name):
    return dogee.get_address_balance(labels=name)["data"]["balances"][0]

def send_money(amount, from_name, to_name): # All args as strings
    RES=dogee.prepare_transaction(amounts=amount, from_labels=from_name, to_labels=to_name)
    summary=dogee.summarize_prepared_transaction(RES)
    summary=float(summary["network_fee"])+float(summary["blockio_fee"])
    SIGN=dogee.create_and_sign_transaction(RES)
    dogee.submit_transaction(transaction_data=SIGN)
    return summary

def calculate_money_fee(amount, from_name, to_name):
    RES=dogee.prepare_transaction(amounts=amount, from_labels=from_name, to_labels=to_name)
    summary=dogee.summarize_prepared_transaction(RES)
    summary=float(summary["network_fee"])+float(summary["blockio_fee"])
    return summary
    
def calculate_address_fee(amount, from_name, to_address):
    RES=dogee.prepare_transaction(amounts=amount, from_labels=from_name, to_addresses=to_address)
    summary=dogee.summarize_prepared_transaction(RES)
    summary=float(summary["network_fee"])+float(summary["blockio_fee"])
    return summary

def send_money_to_address(amount, from_name, to_address):
    RES=dogee.prepare_transaction(amounts=amount, from_labels=from_name, to_addresses=to_address)
    summary=dogee.summarize_prepared_transaction(RES)
    summary=float(summary["network_fee"])+float(summary["blockio_fee"])
    SIGN=dogee.create_and_sign_transaction(RES)
    dogee.submit_transaction(transaction_data=SIGN)
    return summary

def get_current_price():
    return dogee.get_current_price()

#create_new_wallet("enes")
#info=get_wallet_info("default")
#print(info["address"], info["available_balance"])
#print(send_money("10", "default", "saitama1"))
#print(calculate_money_fee("8", "default", "saitama"))