import socket

import serial


def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    print("Server: Starting the control server...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(("192.168.1.103", 8080))

    while True:
        data, addr = sock.recvfrom(1024)
        ser.write(data)


if __name__ == "__main__":
    main()
