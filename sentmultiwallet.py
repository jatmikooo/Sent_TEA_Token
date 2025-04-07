import pandas as pd
import time
import random
from datetime import datetime
from web3 import Web3

RPC = "https://tea-sepolia.g.alchemy.com/public"
CHAIN_ID = 10218
GAS = 21000
MAX_TX = 1000

df = pd.read_csv("address.csv")
if 'address' not in df.columns:
    raise Exception("Kolom 'address' tidak ditemukan di cleaned_address.csv")

addresses = [Web3.to_checksum_address(addr.strip()) for addr in df['address'].dropna().unique()]

with open("pk_wallet.txt", "r") as f:
    private_keys = [line.strip() for line in f if line.strip()]

if not private_keys:
    raise Exception("Tidak ada private key ditemukan di pk_wallet.txt")

print(f"🔑 Total wallet: {len(private_keys)} | 🎯 Total address tujuan: {len(addresses)}")

w3 = Web3(Web3.HTTPProvider(RPC))
accounts = [w3.eth.account.from_key(pk) for pk in private_keys]
done_files = {acc.address: f"done_{acc.address}.txt" for acc in accounts}

sent_map = {}
for acc in accounts:
    try:
        with open(done_files[acc.address], "r") as f:
            sent_map[acc.address] = set(line.strip().lower() for line in f)
    except FileNotFoundError:
        sent_map[acc.address] = set()

tx_counter = 0  

for i, to_address in enumerate(addresses):
    if tx_counter >= MAX_TX:
        print(f"\n🚫 Batas {MAX_TX} transaksi tercapai. Bot berhenti.")
        break

    if all(to_address.lower() in sent_map[acc.address] for acc in accounts):
        continue

    print(f"\n📦 Kirim ke address [{i+1}/{len(addresses)}]: {to_address}")

    wallet_zipped = list(zip(accounts, private_keys))
    random.shuffle(wallet_zipped) 

    for acc, pk in wallet_zipped:
        if tx_counter >= MAX_TX:
            print(f"\n🚫 Batas {MAX_TX} transaksi tercapai. Bot berhenti.")
            break

        wallet_index = accounts.index(acc) + 1

        if to_address.lower() in sent_map[acc.address]:
            print(f"[wallet {wallet_index}] ⏭️ Sudah dikirim sebelumnya.")
            continue

        try:
            nonce = w3.eth.get_transaction_count(acc.address)
            gas_price_gwei = random.randint(8, 15)
            
            send_amount = round(random.uniform(0.1, 0.3), 4)

            tx = {
                'to': to_address,
                'value': w3.to_wei(send_amount, 'ether'),
                'gas': GAS,
                'gasPrice': w3.to_wei(gas_price_gwei, 'gwei'),
                'nonce': nonce,
                'chainId': CHAIN_ID
            }

            start_time = time.time()
            signed_tx = w3.eth.account.sign_transaction(tx, pk)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            end_time = time.time()

            waktu = datetime.now().strftime("%H:%M:%S")
            durasi = round(end_time - start_time, 4)
            saldo = w3.from_wei(w3.eth.get_balance(acc.address), 'ether')
            gas_used = receipt.gasUsed
            tx_counter += 1

            print(f"[wallet {wallet_index}] ✅ {send_amount} TEA → {to_address} | TX: {tx_hash.hex()} | ⛽ Gas Used: {gas_used} | 🪙 Gas Price: {gas_price_gwei} Gwei | 🕒 {waktu} | ⌛ {durasi}s | 💰 {saldo:.5f} TEA | 🔢 TX #{tx_counter}/{MAX_TX}")

            with open(done_files[acc.address], "a") as f:
                f.write(to_address.lower() + "\n")
            sent_map[acc.address].add(to_address.lower())

            time.sleep(random.uniform(2, 10)) 
        except Exception as e:
            print(f"[wallet {wallet_index}] ⚠️ Gagal kirim: {e}")

    delay = random.uniform(5, 15)  
    print(f"⏳ Delay {delay:.2f} detik sebelum transaksi selanjutnya...")
    time.sleep(delay)

print("\n✅ Proses selesai.")

