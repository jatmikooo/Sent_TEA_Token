# Sent TEA Token - Multi Wallet Sender

Script Python untuk mengirim token native TEA (Testnet Sepolia) ke banyak address sekaligus menggunakan banyak wallet (private key).


##  Fitur

- Kirim token TEA ke ribuan address dari file `address.csv`
- Menggunakan banyak private key dari file `pk_wallet.txt`
- Round-robin: setiap address dikirim dari wallet berbeda
- Resume otomatis jika script dihentikan
- Tampil log realtime + saldo sisa wallet
- Support RPC TEA Sepolia: `https://tea-sepolia.g.alchemy.com/public`


## Requirement

- Python 3.10
- `web3` versi 5.31.4
- `pandas`

###  Install Dependesi:

pip install web3==5.31.4 pandas


## 🚀 Cara Menjalankan

1. Siapkan address tujuan
   Format file `address.csv`:
   

2. Siapkan private key
   File `pk_wallet.txt` berisi daftar private key. Satu baris satu private key:
   
   0xabc123...
   0xdef456...
   

3. Jalankan script:
   jika yang terinstall sudah versi 3.10:

   python sentmultiwallet.py

   jika ada beberapa versi python, script ini menggunakan versi 3.10:

   py -3.10 sentmultiwallet.py