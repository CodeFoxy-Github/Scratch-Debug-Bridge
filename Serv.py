import logging
import time
import threading
import sys
import ctypes
import websocket
import socket
import argparse
from websocket_server import WebsocketServer
import os
from termcolor import colored

# Globals
stop = False
server_thread = None
server = None
connected_clients = []
client_even_1 = False

# Argument Parser
parser = argparse.ArgumentParser(
    prog="sdb",
    description="A remote debugger similar to adb but for Scratch",
    epilog="Goodbye!"
)

parser.add_argument(
    "-s",
    "--shell",
    action="store_true",
    help="Run SDB shell."
)

parser.add_argument(
    "-c",
    "--cmds",
    action="store_true",
    help="See SDB commands."
)

parser.add_argument(
    "-r",
    "--run",
    nargs=argparse.REMAINDER,
    help="Run SDB command."
)

args = parser.parse_args()

def helpz():
    """Display help information."""
    print("\nCommands available:")
    print("Variables:")
    print("  var")
    print("     add <var name>          - Add a new variable with the specified name.")
    print("     del <var name>          - Delete the variable with the specified name.")
    print("     pos <var name> <x> <y>  - Set the position of the variable.")
    print("     list                    - List all variables.")
    print("     show <var name>         - Show the specified variable.")
    print("     hide <var name>         - Hide the specified variable.")
    
    print("\nSprites:")
    print("  pos <sprite name> <x> <y>  - Set the position of the sprite.")
    print("  get <sprite name>          - Get information about the sprite.")
    print("    x                        - Get the x position of the sprite.")
    print("    y                        - Get the y position of the sprite.")
    print("    size                     - Get the size of the sprite.")
    print("    dir                      - Get the direction of the sprite.")
    print("    costume #                - Get the costume number of the sprite.")
    print("    direction                - Get the direction of the sprite.")
    print("  list                       - List all sprites.")
    
    print("\nUtilities:")
    print("  echo <data>            - Echo the specified data.")
    print("  clear                  - Clear the shell screen.")
    print("  help                   - Display this help message.")
    print("    sprite               - Display help for sprite commands.")
    print("    var                  - Display help for variable commands.")
    print("  flag                   - Click The Green flag in Scratch.")
    print("  restart                - Restart the project.")
    print("  stop                   - Stop the project.")

    print("\nEnvironment variables:")
    print("  env                    - Environment variables (e.g., ${name})")
    print("    list                 - List all environment variables.")
    print("    set <name> <value>   - Set an environment variable.")
    print("    del <name>           - Delete an environment variable.")
    print("    clear                - Clear environment variables that are not System Placeholders.")
    
    print("\nSystem Placeholders:")
    print("  ${random}              - A random 2-digit number.")
    print("  ${hr}                  - The current hour.")
    print("  ${min}                 - The current minute.")
    print("  ${sec}                 - The current second.")
    print("  ${year}                - The current year.")
    print("  ${month}               - The current month.")
    print("  ${day}                 - The current day.")
    print("  ${week}                - The current week.")
    print("  ${env}                 - All environment variables.")
    print("  ${url}                 - The URL of the current web page.")
    print("  ${browser}             - The name of the current browser.")
    print("  ${system}              - The operating system.")
    print("  ${battery}             - The current battery level.")
    print("  ${turbo}               - The turbo mode status.")
    print("  ${internet}            - The current internet connection status.")
    print("  ${fps}                 - The frames per second of the current environment.")
    print("  ${delta}               - The delta time since the last frame.")
    print("  ${clone}               - The number of clones of the sprite.")
    print("  ${width}               - The width of the current stage or sprite.")
    print("  ${height}              - The height of the current stage or sprite.")
    print("  ${<variable name>}     - Value of the specified environment variable.")

def clear_line():
    """Clear the current line in the shell."""
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def message_handler(client, server, message):
    """Handle incoming messages from clients."""
    global client_even_1
    client_even_1 = True
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
    elif "/errno: " in message:
        print(colored(message.replace("/errno: ", ""), 'light_red'))
        print(colored("<sdb>: ", 'light_red'), end="")
    elif "/warno: " in message:
        print(colored(message.replace("/warno: ", ""), 'light_yellow'))
        print(colored("<sdb>: ", 'light_yellow'), end="")
    elif "/donern/s " in message:
        print(colored("Success!", "light_blue"))
        print("<sdb>: ", end="")
    elif "tmsf r" in message:
        print(colored(message.replace("tmsf r", ""), 'light_cyan'))
        print("<sdb>: ", end="")
        sys.stdout.flush()
    else:
        clear_line()
        print(f"Client {client['id']}: {message}")
        print("<sdb>: ", end="")
        sys.stdout.flush()

def client_disconnect(client, server):
    """Handle client disconnection."""
    clear_line()
    print("<sdb>: ", end="")
    print(colored(f"Client {client['id']} has left.", "light_red"))
    print("<sdb>: ", end="")
    sys.stdout.flush()
    global client_even_1
    client_even_1 = False

def new_client_connection(client, server):
    """Handle new client connection."""
    clear_line()
    print("<sdb>: ", end="")
    print(colored(f"Client {client['id']} has joined.", "light_blue"))
    print("<sdb>: ", end="")
    sys.stdout.flush()
    global client_even_1
    client_even_1 = True
    connected_clients.append(client)

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

def daemon():
    print("Starting the daemon...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
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
        # Initialize and start the WebSocket server
        global server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(f"Connect to {colored("ws://localhost:4328", 'light_yellow')} or {colored(s.getsockname()[0] + ":4328", 'light_yellow')}.")
        s.close()
        server = WebsocketServer(host='127.0.0.1', port=4328, loglevel=logging.ERROR)
        server.set_fn_message_received(message_handler)
        if args.run is None:
            server.set_fn_client_left(client_disconnect)
            server.set_fn_new_client(new_client_connection)
        initiate_server()
    except Exception as e:
        logging.error(f"Error initializing server: {e}")
        sys.exit(1)

if not any(vars(args).values()):
    parser.print_help()
else:
    if args.cmds:
        helpz()

if args.shell:
    os.system('title Scratch Debug Bridge' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'PS1=\'\\[\\e]0;Scratch Debug Bridge\\a\\]\\u@\\h\\w\\$\'')
    print("Scratch Debug Bridge")
    print("By: Codefoxy")
    daemon()
    try:
        while not stop:
            clear_line()
            user_input = input("<sdb>: ")
            clear_line()
            if user_input == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
            elif user_input == "help":
                helpz()
            elif user_input == "exit":
                server.shutdown_gracefully()
                stop = True
                print("\nDaemon stopped.")
                server_thread.raise_exception()
                server_thread.join()
            else:
                server.send_message_to_all(user_input)
                if not client_even_1:
                    print(colored("Warning: No client connected!", 'light_yellow'))
                    print(colored("<sdb>: ", 'light_yellow'), end="")
            time.sleep(0.09)
    except KeyboardInterrupt:
        server.shutdown_gracefully()
        stop = True
        print("\nDaemon stopped.")
        server_thread.raise_exception()
        server_thread.join()
        sys.exit(0)
elif args.run is not None:
    daemon()
    while not client_even_1:
        time.sleep(0.01)
    run_command = ' '.join(args.run)
    for client in connected_clients:
        server.send_message(client, run_command)
    server.disconnect_clients_abruptly()
