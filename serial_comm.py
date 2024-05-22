import serial
import time

arduino = None

def init(port):
    arduino = serial.Serial(port, baudrate=9600)

def write(message):
    arduino.write(bytes(message, 'utf-8'))
    return

if __name__ == "__main__":
    while True:
        i = input('Enter 0 or 1: ')
        write(i)
        time.sleep(0.2)