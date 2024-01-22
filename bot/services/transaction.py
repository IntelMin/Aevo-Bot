import time
import threading
import asyncio
from queue import Queue
from web3 import Web3

from utils.formatting import wei_to_eth
from utils.alert import send_telegram_alert

transaction_queue = Queue()

def process_transactions():
    while True:
        print("Processing transactions...")
        # action, object = transaction_queue.get()
        
        time.sleep(3)
        
        transaction_queue.task_done()
        time.sleep(0.5)

# Start a thread to process transactions
transaction_thread = threading.Thread(target=process_transactions)

def initalize_queue():
    transaction_thread.start()

