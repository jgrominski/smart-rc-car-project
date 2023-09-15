# Smart RC Car Project
A project aimed at creating a smart RC car from scratch. Currently a working prototype, the project consists of a desktop client app, server-side software for a Raspberry Pi used to stream the onboard camera in real time via RTSP and pass control inputs from the client to a microcontroller, and an Arduino software for taking and executing steering instructions.

## Usage
1. Ensure everything is correctly connected, and turned on
2. Run `rtsp_server.py` and `control_server.py` files on the Raspberry Pi
3. Run `client.py` on the client
