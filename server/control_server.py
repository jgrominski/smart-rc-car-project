import socket

import serial


def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    print("Server: Starting the control server...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(("", 8080))

    while True:
        data, addr = sock.recvfrom(1024)
        cmds = data.split()
        for cmd in cmds:
            ser.write(cmd)


if __name__ == "__main__":
    main()
