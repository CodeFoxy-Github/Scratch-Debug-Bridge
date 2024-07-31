import logging
import time
import threading
import sys
import ctypes
import websocket
import json
import socket
from websocket_server import WebsocketServer
import os
from termcolor import colored
global stop
stop = False
def clear_line():
    """Clear the current line in the terminal."""
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def message_handler(client, server, message):
    """Handle incoming messages from clients."""
    if message == "heartbeat.ping":
        server.send_message(client, "pong")
        logging.info(f"Client {client['id']} sent a ping!")
    elif message == "heartbeat.are u awake":
        server.send_message(client, "yes")
        logging.info(f"Client {client['id']} inquired if we're awake!")
    elif message == "splsleave":
        global stop
        stop = True
        server.shutdown_gracefully()
        print("\nDaemon stopped.")
        server_thread.raise_exception()
        server_thread.join()
        sys.exit()
    elif message.find("/errno: ") == -1 and message.find("/warno: ") == -1:
        clear_line()
        print(f"Client {client['id']}: {message}")
        print("<sdb>: ", end="")
        sys.stdout.flush()
    elif message.find("/warno: ") == -1:
        print(colored(message.replace("/errno: ", ""), 'light_red'))
        print(colored("<sdb>: ", 'light_red'), end="")
    else:
        print(colored(message.replace("/warno: ", ""), 'light_yellow'))
        print(colored("<sdb>: ", 'light_yellow'), end="")

def client_disconnect(client, server):
    """Handle client disconnection."""
    clear_line()
    print(f"Client {client['id']} has left.")
    print("<sdb>: ", end="")
    sys.stdout.flush()

def new_client_connection(client, server):
    """Handle new client connection."""
    clear_line()
    print(f"Client {client['id']} has joined.")
    print("<sdb>: ", end="")
    sys.stdout.flush()

class WebSocketServerThread(threading.Thread):
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

def initiate_server():
    """Start the WebSocket server thread."""
    global server_thread
    server_thread = WebSocketServerThread('WebSocketServerThread')
    server_thread.start()

print("Starting the daemon...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', 4328))
if result == 0:
    print("Daemon is already running. Stopping it now.")
    sock.close()
    quit_websocket = websocket.WebSocket()
    quit_websocket.connect("ws://localhost:4328")
    quit_websocket.send("splsleave")
    quit_websocket.close()
else:
    sock.close()
os.system('cls' if os.name == 'nt' else 'clear')
# Initialize and start the WebSocket server
server = WebsocketServer(host='127.0.0.1', port=4328, loglevel=logging.ERROR)
server.set_fn_message_received(message_handler)
server.set_fn_client_left(client_disconnect)
server.set_fn_new_client(new_client_connection)

initiate_server()
print("Scratch Debug Bridge")
print("By: Codefoxy")
try:
    while stop == False:
        clear_line()
        user_input = input("<sdb>: ")
        clear_line()
        if user_input == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
        elif user_input == "help":
            print("\nvar: ")
            print("     add <var name>")
            print("     del <var name>")
            print("     pos <var name> <x> <y>")
            print("     list")
            print("     show <var name>")
            print("     hide <var name>")
            print("sprite:")
            print("     pos <sprite name> <x> <y>")
            print("     get <sprite name>")
            print("         x")
            print("         y")
            print("         size")
            print("         dir")
            print("         costume #")
            print("         direction")
            print("     list")
            print("utils:")
            print("     echo <data>")
            print("     clear")
            print("     help")
            print("         sprite")
            print("         var")
            print("     ")
            print("${random} a random 2 number")
            print("${hr} now hour")
            print("${min} now minute")
            print("${sec} now second\n")
            print("${year} a random 4 number")
            print("${month} now hour")
            print("${day} now minute")
            print("${week} now second")
        else:
            server.send_message_to_all(user_input)
        time.sleep(0.09)

except KeyboardInterrupt:
    server.shutdown_gracefully()
    stop = True
    print("\nDaemon stopped.")
    server_thread.raise_exception()
    server_thread.join()
