import logging
import socket
import time
import threading
import sys
import ctypes
import websocket
import json
from websocket_server import WebsocketServer

def clear_console_line():
    """Clear the current line in the terminal."""
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def handle_message(client, server, message):
    """Handle incoming messages from clients."""
    if message == "heartbeat.ping":
        server.send_message(client, "pong")
        logging.info(f"Client {client['id']} sent a ping!")
    elif message == "heartbeat.are u awake":
        server.send_message(client, "yes")
        logging.info(f"Client {client['id']} inquired if we're awake!")
    elif message == "splsleave":
        print("\nDaemon stopped.")
        server_thread.raise_exception()
        server_thread.join()
        sys.exit()
    else:
        clear_console_line()
        print(f"<sdb> {client['id']}: {message}")
        print("<sdb>: ", end="")
        sys.stdout.flush()

def client_left(client, server):
    """Handle client disconnection."""
    clear_console_line()
    print(f"Client {client['id']} has left.")
    print("<sdb>: ", end="")
    sys.stdout.flush()

def new_client(client, server):
    """Handle new client connection."""
    clear_console_line()
    print(f"Client {client['id']} has joined.")
    print("<sdb>: ", end="")
    sys.stdout.flush()

class ServerThread(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)
        self.name = name

    def run(self):
        """Run the WebSocket server."""
        try:
            server.run_forever()
        finally:
            print('Server has stopped.')

    def get_id(self):
        """Retrieve the thread ID."""
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
        return None

    def raise_exception(self):
        """Raise an exception in the thread."""
        thread_id = self.get_id()
        if thread_id is not None:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Failed to raise the exception.')

def start_server():
    """Start the WebSocket server thread."""
    global server_thread
    server_thread = ServerThread('ServerThread')
    server_thread.start()

print("########################")
print("# Scratch Debug Bridge #")
print("#        V2.4          #")
print("#    By: Codefoxy      #")
print("########################")

# Check if the daemon is already running
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', 7420))
if result == 0:
    print("Daemon is already running. Stopping it now.")
    sock.close()
    helpquit = websocket.WebSocket()
    helpquit.connect("ws://localhost:7420")
    helpquit.send("splsleave")
    helpquit.close()
    print("Error: Unable to stop the daemon. Please close it manually and press enter.")
    a = input()
else:
    print("Starting the daemon...")
    sock.close()

# Initialize and start the WebSocket server
server = WebsocketServer(host='127.0.0.1', port=7420, loglevel=logging.ERROR)
server.set_fn_message_received(handle_message)
server.set_fn_client_left(client_left)
server.set_fn_new_client(new_client)

start_server()

try:
    while True:
        clear_console_line()
        user_input = input("<sdb>: ")
        clear_console_line()
        print("<sdb>: ", end="")
        server.send_message_to_all(user_input)
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nDaemon stopped.")
    server_thread.raise_exception()
    server_thread.join()
