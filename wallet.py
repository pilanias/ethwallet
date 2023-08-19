import sqlite3
from eth_account import Account
import sys

def create_wallets_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY,
            address TEXT UNIQUE
        )
    ''')
    conn.commit()

def insert_address(conn, address):
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO wallets (address) VALUES (?)', (address,))
    conn.commit()

def check_address_exists(conn, address):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM wallets WHERE address = ?', (address,))
    count = c.fetchone()[0]
    return count > 0

def generate_and_check_wallets(conn, num_wallets):
    # Enable unaudited HD wallet features
    Account.enable_unaudited_hdwallet_features()

    for i in range(num_wallets):
        acct, mnemonic = Account.create_with_mnemonic()

        wallet_address = acct.address
        print(f"Checking wallet {i+1}:")
        
        if check_address_exists(conn, wallet_address):
            print("Address already exists in the database.")
            print("Address:", wallet_address)
            print("Seed Phrase (Mnemonic):", mnemonic)
            sys.exit("Program terminated because address exists in the database.")
        else:
            print("Not found generating again.")
        
        print("---")

if __name__ == "__main__":
    num_wallets_to_generate = 500000

    # Connect to the SQLite database
    db_connection = sqlite3.connect("eth_addresses.db")
    create_wallets_table(db_connection)

    generate_and_check_wallets(db_connection, num_wallets_to_generate)

    db_connection.close()
