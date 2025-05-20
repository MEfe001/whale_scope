import curses
import asyncio
import json
import websockets
import time
import os
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal
from eth_utils import decode_hex
from web3 import Web3

# Load .env file
load_dotenv()

# Program name
PROGRAM_NAME = "WhaleScope"

# Output file
OUTPUT_FILE = "whale_transactions_log.txt"

# Minimum ETH value for whale alert
MIN_ETH_VALUE = 50

# Known DEX router addresses (e.g., Uniswap, SushiSwap)
DEX_ROUTERS = {
    "0xf164fc0ec4e93095b804a4795bbe1e041497b92a": "UniswapV2",
    "0xe592427a0aece92de3edee1f18e0157c05861564": "UniswapV3",
    "0x1b02da8cb0d097eb8d57a175b88c7d8b47997506": "SushiSwap"
}

# Infura Project ID from .env
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
INFURA_WSS_URL = f"wss://mainnet.infura.io/ws/v3/{INFURA_PROJECT_ID}"
INFURA_HTTPS_URL = f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"

# Initialize Web3 HTTP instance for token name lookup
w3 = Web3(Web3.HTTPProvider(INFURA_HTTPS_URL))

# Global transaction buffer
recent_whale_txs = []

# Helper to decode token being bought from Uniswap input and fetch name if unknown
def identify_token_from_input(input_data):
    try:
        if len(input_data) < 138:
            return None
        token_address = "0x" + input_data[-40:].lower()
        try:
            contract = w3.eth.contract(address=token_address, abi=[{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}])
            symbol = contract.functions.symbol().call()
            return symbol
        except Exception:
            return token_address[:10] + "..."
    except Exception:
        return None

# Save to file
def save_transaction_to_file(tx):
    with open(OUTPUT_FILE, "a") as f:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        line = f"[{timestamp}] From: {tx['from']} -> To: {tx['to']} | Value: {tx['value']:.2f} ETH | Type: {tx['type']} | Hash: {tx['hash']}\n"
        f.write(line)

# Async function to listen to mempool transactions
def listen_to_mempool():
    async def run():
        global recent_whale_txs

        if not INFURA_PROJECT_ID:
            return  # Skip if no valid key

        async with websockets.connect(INFURA_WSS_URL) as ws:
            subscribe_msg = json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_subscribe",
                "params": ["newPendingTransactions"]
            })
            await ws.send(subscribe_msg)

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=60)
                    data = json.loads(message)
                    if 'params' in data:
                        tx_hash = data['params']['result']

                        get_tx_msg = json.dumps({
                            "jsonrpc": "2.0",
                            "id": 2,
                            "method": "eth_getTransactionByHash",
                            "params": [tx_hash]
                        })
                        await ws.send(get_tx_msg)
                        tx_detail_msg = await asyncio.wait_for(ws.recv(), timeout=10)
                        tx_data = json.loads(tx_detail_msg)
                        tx = tx_data.get("result")

                        if tx:
                            eth_value = int(tx.get("value", "0x0"), 16) / 1e18
                            to_addr = tx.get("to", "").lower()
                            tx_input = tx.get("input", "0x")

                            is_token_swap = to_addr in DEX_ROUTERS
                            is_large_eth = eth_value >= MIN_ETH_VALUE

                            token_name = None
                            if is_token_swap and eth_value > 0:
                                token_name = identify_token_from_input(tx_input)

                            if is_large_eth or is_token_swap:
                                tx_note = "ETH Transfer"
                                if is_token_swap and eth_value > 0:
                                    tx_note = f"Swap via {DEX_ROUTERS[to_addr]}"
                                    if token_name:
                                        tx_note += f" (buying {token_name})"

                                entry = {
                                    "from": tx.get("from", "N/A"),
                                    "to": to_addr,
                                    "value": eth_value,
                                    "hash": tx.get("hash", ""),
                                    "type": tx_note
                                }
                                recent_whale_txs.append(entry)
                                save_transaction_to_file(entry)
                                recent_whale_txs = recent_whale_txs[-50:]
                except Exception:
                    continue

    return run()

# Format a whale transaction for display
def format_whale_transaction(tx):
    return f"From: {tx['from'][:12]}... To: {tx['to'][:12]}... Value: {tx['value']:>8.2f} ETH  Type: {tx['type']}  Hash: {tx['hash'][:10]}..."

# Curses UI for displaying transactions
def display_whale_transactions(screen):
    global recent_whale_txs
    curses.curs_set(0)
    screen.nodelay(True)
    screen.timeout(100)

    while True:
        screen.clear()
        screen.addstr(0, 0, f"{PROGRAM_NAME} - LIVE MEMPOOL WHALE WATCHER - Showing transactions over {MIN_ETH_VALUE} ETH", curses.color_pair(1) | curses.A_BOLD)
        screen.addstr(1, 0, "=" * 106, curses.color_pair(1) | curses.A_BOLD)
        screen.addstr(2, 0, "Listening to mempool...", curses.color_pair(1))
        screen.addstr(3, 0, "=" * 106, curses.color_pair(1))
        screen.addstr(4, 0, "This tool is for informational purposes only. Always verify on-chain data independently.", curses.color_pair(1))
        screen.addstr(5, 0, "=" * 106, curses.color_pair(1))

        if not INFURA_PROJECT_ID:
            screen.addstr(7, 0, "⚠️  Please provide a valid Infura WebSocket Project ID in .env", curses.color_pair(2))
        elif not recent_whale_txs:
            screen.addstr(7, 0, "No large ETH transfers or token swaps detected yet...", curses.color_pair(2))
        else:
            for idx, tx in enumerate(recent_whale_txs[-(curses.LINES - 8):]):
                screen.addstr(7 + idx, 0, format_whale_transaction(tx), curses.color_pair(2))

        screen.refresh()
        time.sleep(1)

# Initialize curses colors
def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

# Main entry point (runs asyncio and curses in parallel)
def main(screen):
    init_colors()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(listen_to_mempool())
    try:
        display_whale_transactions(screen)
    finally:
        loop.stop()
        loop.close()

curses.wrapper(main)
