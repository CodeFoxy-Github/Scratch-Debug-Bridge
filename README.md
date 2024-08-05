 

# Scratch Debug Bridge (SDB)

A remote debugger similar to adb but for Scratch. This tool allows you to connect to and debug Scratch projects remotely.

## Features

*   Connect to Scratch projects remotely
*   Execute commands and receive responses
*   Manage variables and sprites
*   Environment variables and system placeholders

## Requirements

*   Python 3.x
*   Required Python packages: `websocket-server`, `termcolor`, `websocket-client`

## Installation

1.  Clone the repository:
    
    ```
    git clone https://github.com/CodeFoxy-Github/Scratch-Debug-Bridge
    ```
    
2.  Navigate to the project directory:
    
    ```
    cd Scratch-Debug-Bridge
    ```
    
3.  Install the required packages:
    
    ```
    pip install websocket-server termcolor websocket-client
    ```
    

## Usage

### Build (if on Linux)

If you are running on Linux, ensure you give execute permissions to the build script first.

Then, open the `Package` directory and click on your OS's one-click build script (e.g., `"(Your OS) One Click Build.bat"`).

### Running SDB

You can run SDB in different modes using the command line arguments.

#### Running the SDB Shell

```
python sdb.py -s
```

#### Viewing SDB Commands

```
python sdb.py -c
```

#### Running SDB Commands

```
python sdb.py -r <command>
```
