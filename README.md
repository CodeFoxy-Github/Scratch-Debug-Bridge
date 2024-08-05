 

# Scratch Debug Bridge (SDB)

A remote debugger similar to adb but for Scratch. This tool allows you to connect to and debug Scratch projects remotely.

## Features

*   Connect to Scratch projects remotely
*   Execute commands and receive responses
*   Manage variables and sprites
*   Environment variables and system placeholders

## Requirements

*   Python 3.x
*   (Will Auto Install Python packages)


## Usage

### Build

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
