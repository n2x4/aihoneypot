import sys
import threading
import time
import libsql_client
from paramiko import ServerInterface, RSAKey, Transport, AUTH_FAILED
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Set up the Turso-hosted database
url = "libsql://your-database.turso.io"
auth_token = "your-auth-token"
client = libsql_client.create_client_sync(url=url, auth_token=auth_token)

# Create the table if not exists
client.execute("""
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        username TEXT,
        password TEXT,
        ip_address TEXT
    )
""")

class SSHHoneypot(ServerInterface):
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def check_auth_password(self, username, password):
        # Log the login attempt to the Turso-hosted database
        client.execute("""
            INSERT INTO login_attempts (username, password, ip_address)
            VALUES (?, ?, ?)
        """, (username, password, self.ip_address))

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
        try:
            client_socket, addr = server_socket.accept()
            transport = Transport(client_socket)
            transport.add_server_key(host_key)
            transport.start_server(server=SSHHoneypot(addr[0]))
        except EOFError:
            print(f"Error reading SSH protocol banner from {addr[0]}:{addr[1]}")
            transport.close()
        except Exception as e:
            print(f"Exception caught in start_honeypot_server: {e}")
            transport.close()

if __name__ == "__main__":
    try:
        start_honeypot_server()
    except KeyboardInterrupt:
        print("Shutting down honeypot server")
        client.close()  # Close the Turso database client
        sys.exit(0)
