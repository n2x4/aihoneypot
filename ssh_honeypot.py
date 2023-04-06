import sqlite3
import sys
import threading
import time
from paramiko import ServerInterface, RSAKey, Transport, AUTH_FAILED
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Set up the SQLite database
conn = sqlite3.connect("login_attempts.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        username TEXT,
        password TEXT,
        ip_address TEXT
    )
""")
conn.commit()

class SSHHoneypot(ServerInterface):
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def check_auth_password(self, username, password):
        # Log the login attempt to the SQLite database
        conn = sqlite3.connect("login_attempts.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO login_attempts (username, password, ip_address)
            VALUES (?, ?, ?)
        """, (username, password, self.ip_address))
        conn.commit()
        conn.close()

        # Print the login attempt to the terminal
        print(f"Login attempt: {self.ip_address} - {username}:{password}")

        return AUTH_FAILED

def start_honeypot_server():
    host_key = RSAKey.generate(2048)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 2222))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        transport = Transport(client_socket)
        transport.add_server_key(host_key)
        transport.start_server(server=SSHHoneypot(addr[0]))

if __name__ == "__main__":
    try:
        start_honeypot_server()
    except KeyboardInterrupt:
        print("Shutting down honeypot server")
        sys.exit(0)
