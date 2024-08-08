 

# Scratch Debug Bridge (SDB)

Latest Build Status: [![Build](https://github.com/CodeFoxy-Github/Scratch-Debug-Bridge/actions/workflows/Build.yaml/badge.svg)](https://github.com/CodeFoxy-Github/Scratch-Debug-Bridge/actions/workflows/Build.yaml)
</br>
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
But you need to make sure the Sdb sprite is running
#### Running the SDB Shell

```
sdb -s
```

#### Viewing SDB Commands

```
sdb -c
```

#### Running SDB Commands
#### (Buggy)
```
sdb -r <command>
```

# Commands Available

## Variables:

```
var
   add <var name>          - Add a new variable with the specified name.
   del <var name>          - Delete the variable with the specified name.
   pos <var name> <x> <y>  - Set the position of the variable.
   list                    - List all variables.
   show <var name>         - Show the specified variable.
   hide <var name>         - Hide the specified variable.
```

## Sprites:

```
pos <sprite name> <x> <y>  - Set the position of the sprite.
get <sprite name>          - Get information about the sprite.
  x                        - Get the x position of the sprite.
  y                        - Get the y position of the sprite.
  size                     - Get the size of the sprite.
  dir                      - Get the direction of the sprite.
  costume #                - Get the costume number of the sprite.
  direction                - Get the direction of the sprite.
list                       - List all sprites.
```

## Utilities:

```
echo <data>            - Echo the specified data.
clear                  - Clear the shell screen.
help                   - Display this help message.
  sprite               - Display help for sprite commands.
  var                  - Display help for variable commands.
flag                   - Click The Green flag in Scratch.
restart                - Restart the project.
stop                   - Stop the project.
```

## Environment variables:

```
env                    - Environment variables (e.g., ${name})
  list                 - List all environment variables.
  set <name> <value>   - Set an environment variable.
  del <name>           - Delete an environment variable.
  clear                - Clear environment variables that are not System Placeholders.
```

## System Placeholders:

```
${random}              - A random 2-digit number.
${hr}                  - The current hour.
${min}                 - The current minute.
${sec}                 - The current second.
${year}                - The current year.
${month}               - The current month.
${day}                 - The current day.
${week}                - The current week.
${env}                 - All environment variables.
${url}                 - The URL of the current web page.
${browser}             - The name of the current browser.
${system}              - The operating system.
${battery}             - The current battery level.
${turbo}               - The turbo mode status.
${internet}            - The current internet connection status.
${fps}                 - The frames per second of the current environment.
${delta}               - The delta time since the last frame.
${clone}               - The number of clones of the sprite.
${width}               - The width of the current stage or sprite.
${height}              - The height of the current stage or sprite.
${<variable name>}     - Value of the specified environment variable.
```
