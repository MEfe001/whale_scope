# 🐋 WhaleScope (`whalescope.py`)

**WhaleScope** is a real-time Ethereum monitoring tool for tracking large on-chain transactions ("whales"). It listens to the mempool using Infura WebSocket and displays any ETH transactions over a specified threshold or large token purchases via decentralized exchanges (DEX).

---

## ⚙️ Features

- Monitors Ethereum mempool via WebSocket
- Displays transactions exceeding **50 ETH**
- Detects token purchases through Uniswap/SushiSwap
- Automatically extracts token symbols from contract
- Terminal-based visual output using `curses`
- Logs each transaction to a `whale_transactions_log.txt` file

---

## 🛠️ Setup

### 1. 🧪 Requirements:

Install all required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install web3 websockets python-dotenv
```


Or manually:
```bash
pip install web3 websockets
```

### 2. 🔑 Infura API Key Setup:

Create a `.env` file in the project root directory with the following content:
```env
INFURA_PROJECT_ID=your_infura_project_id_here
```

The application will automatically load this variable using `python-dotenv`.

Edit these lines in the file:
```python
INFURA_WSS_URL = "wss://mainnet.infura.io/ws/v3/YOUR_INFURA_PROJECT_ID"
INFURA_HTTPS_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
```

### 3. ▶️ Run:
```bash
python3 whalescope.py
```

Transactions will be shown in the terminal and logged to `whale_transactions_log.txt`.

---

## 📄 Output File

Each transaction is logged in the following format:
```text
[2025-05-18 18:41:27 UTC] From: 0x123... -> To: 0x456... | Value: 78.45 ETH | Type: Swap via UniswapV2 (buying SHIBA) | Hash: 0xabc...
```

File name:
- `whale_transactions_log.txt`

---

## 📃 License

MIT License — see [LICENSE](LICENSE)

---

## ⚠️ Disclaimer

This tool is for **informational and educational purposes only**.

- Many tokens may be deceptive or malicious
- Always do your own research
- The author **accepts no responsibility** for financial loss or misuse
- **Never share your Infura API key**

---

## 💸 Donations

If you find this tool helpful and would like to support further development:

- **Bitcoin (BTC):**  
  `1MorphXyhHpgmYSfvwUpWojphfLTjrNXc7`

- **Monero (XMR):**  
  `86VAmEogaZF5WDwR3SKtEC6HSEUh6JPA1gVGcny68XmSJ1pYBbGLmdzEB1ZzGModLBXkG3WbRv12mSKv4KnD8i9w7VTg2uu`

- **Dash (DASH):**  
  `XtNuNfgaEXFKhtfxAKuDkdysxUqaZm7TDX`

- **Bytecoin (BCN):**  
  `bcnZNMyrDrweQgoKH6zpWaE2kW1VZRsX3aDEqnxBVEQfjNnPK6vvNMNRPA4S7YxfhsStzyJeP16woK6G7cRBydZm2TvLFB2eeR`

🙏 Thank you for supporting independent developers and ethical technology.

> *"I morph bits not to break, but to understand."*  
> — **BitMorphX**