# 🐋 WhaleScope – Release v1.0.0

The first official release of WhaleScope!

---

## 🆕 New Features

- 🔍 Ethereum mempool monitoring using Infura WebSocket
- 🐋 Displays transactions exceeding **50 ETH**
- 💱 Detects token purchases via UniswapV2, UniswapV3, and SushiSwap
- 🧠 Automatically resolves token symbols from smart contracts
- 📺 Terminal display using `curses`
- 📝 All transactions are logged to `whale_transactions_log.txt`

---

## 📄 Files

- `whalescope.py` – main program file
- `requirements.txt` – Python dependencies
- `README.md` – usage instructions
- `LICENSE` – MIT license

---

## ⚠️ Known Limitations

- Does not work in native Windows `cmd` or `PowerShell` — use WSL or Ubuntu instead
- Token names may be unavailable if the contract does not implement `symbol()`
- Requires an active Infura project with WebSocket support

---

## 📦 Installation

```bash
pip install -r requirements.txt
python3 whalescope.py
```

---

## 🙏 Acknowledgments

Thanks to everyone supporting open-source tools. If you'd like to contribute — check the **Donations** section in the README.

> “If something seems invisible to the chain, it doesn’t mean whales aren’t moving it.”  
> — **BitMorphX**
---

## 🔐 API Configuration

This program uses a `.env` file to securely load your Infura WebSocket Project ID.

Create a `.env` file with the following content:

```env
INFURA_PROJECT_ID=your_infura_project_id_here
```

The application automatically loads this variable using the `python-dotenv` library.