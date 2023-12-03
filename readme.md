# LoL Yuumi For All
LoL Yuumi For All is a python project that allows you to control multiple Yuumis simultaneously in One For All mode.  
But this can also be used to control one or multiple other devices for any other purpose.

## Usage
Server script is ran on main device, and client script is ran on up to 4 'slave' devices.  
Every mouse movement, click and keyboard key-press is sent from server to each client and replicated on them.  
This way every controlled Yuumi will do same actions.  
It is recommended to maintain same movement speed for all Yuumis so they don't miss-align from 'swarm'.  
Some keys are not replicated in all clients, they are rather cycled, e.g. only one Yuumi uses heal at a time.  
Modifier keys are not recorded (Ctrl, Shift, Alt...)

## Features
Server has full mouse and keyboard control over all clients  
Press Ctrl+C anytime to stop server  
Client can temporarily toggle control (Ctrl+R)  
Client has global fail-safe key (Ctrl+C)

### TODO
Fire all prowling projectiles to mouse direction  
Cycle prowling projectiles
Attach all client Yuumis to server  
Use all zoomies at once  
Cycle zoomies  
Use one ultimate, cycled  
Attach server and all other Yuumis to backup Yuumi  
Use one R spell, cycled  
Use one D spell, cycled  
Use one F spell, cycled  
Level up separate abilities for all Yuumis  
Open shop button  
Center camera on all Yuumis - used when some clients camera offset from servers due to ping  
Server can toggle controlling all clients  
Full control mode - disables above features and allows all keys on keyboard  
Auto reconnect

## Configuration
Several options can be changed in config.ini, tick should be same for server and client.
### Main config
`server_address` - local address of server and to what address client should connect to  
`server_port` - what port server is listening to, ant to what port client should connect to  
`fps` - limit how many times per second data is collected and sent to client, higher value increases CPU usage (does not limit in-game fps)  
`game_res` - if game is running in lower resolution, set it in server_res to format: `xxxx, yyyy`, anything else will get maximum screen resolution.  
`full_control` - allows server to toggle full control over this client
### Keys config
### TODO
`q, w, e, r, d, f` - keys for casting spells on all Yuumis (r, d, f, are cycled)  
`lvl_up_q, lvl_up_w, lvl_up_e, lvl_up_r` - keys to level up spells on all Yuumis  
`shop` - key to open shop on all Yuumis  
`center` - key used to center camera on champion  
`attach_bkp` - key to attach server and all other Yuumis to backup Yuumi  
`cycle_prowl` - key used to cycle prowling projectiles rather than firing all at once  
`cycle_zoomies` - key used to cycle zoomies rather than casting all at once  
`toggle_control` - key to toggle control over all clients  
`toggle_full_control` - key to toggle full control mode over all clients


## Setup
1. Install [Python](https://www.python.org/)
2. Clone this repository, unzip it
3. Open terminal, cd to unzipped folder
4. Install requirements: `pip install -r requirements.txt`

## Running
To run server, run this command:
```bash
python server.py
```
To run client, run this command:
```bash
python client.py
```
If server and clients are running on same local network get servers ip by running ipconfig in terminal then put it in config `server_address`.  
If not, one who is running server should port forward. If it is not possible - use some alternative way to expose local port (e.g. [Yggdrasil network](https://yggdrasil-network.github.io/)). `server_address` should then be `localhost`  
Make sure that in-game UI is same scale on all devices.  
If game on any device is running in lower resolution than screen, that resolution should be configured in config.ini.
