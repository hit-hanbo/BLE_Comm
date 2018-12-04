from bluepy import *
import tkinter as tk
import struct
from bluepy.btle import DefaultDelegate
import time

header =  0xA2
tail   =  0xCD
zero   =  0x00
left   =  0x40
right  =  0x50

class NotifyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self,cHandle,data):
        print("notify from "+str(cHandle)+str(data)+"\n")


class GUI:

    def __init__(self):
        root = tk.Tk()
        root.geometry('720x540')

        self.dev=btle.Peripheral("a4:c1:38:06:19:6d").withDelegate(NotifyDelegate())

        self.left_direction_entry  = tk.Entry(root, width=80)
        self.left_direction_entry.pack()

        self.left_speed_entry      = tk.Entry(root, width=80)
        self.left_speed_entry.pack()

        self.right_direction_entry = tk.Entry(root, width=80)
        self.right_direction_entry.pack()

        self.right_speed_entry     = tk.Entry(root, width=80)
        self.right_speed_entry.pack()

        button = tk.Button(root, text="Submit",
                            command=self.submit)
        button.pack()

        root.mainloop()

    def submit(self):
        left_direction = self.left_direction_entry.get()
        left_speed = self.left_speed_entry.get()
        right_direction = self.right_direction_entry.get()
        right_speed = self.right_speed_entry.get()

        if(left_direction == '0'):
            left_direction = 0x00
        elif(left_direction == '1'):
            left_direction = 0xFF

        if(right_direction == '0'):
            right_direction = 0xFF
        elif(right_direction == '1'):
            right_direction = 0x00

        left_speed = int(self.left_speed_entry.get()) + 30
        right_speed = int(self.right_speed_entry.get()) + 30

        struct_left_speed = struct.pack('c', bytes([left_speed]))
        struct_right_speed = struct.pack('c', bytes([right_speed]))
        struct_left_direction = struct.pack('c', bytes([left_direction]))
        struct_right_direction = struct.pack('c', bytes([right_direction]))

        struct_header = struct.pack('c', bytes([header]))
        struct_tail = struct.pack('c', bytes([tail]))
        struct_zero = struct.pack('c', bytes([zero]))
        struct_left = struct.pack('c', bytes([left]))
        struct_right = struct.pack('c', bytes([right]))

        self.dev.writeCharacteristic(10, struct_header)
        self.dev.writeCharacteristic(10, struct_left)
        self.dev.writeCharacteristic(10, struct_left_direction)
        self.dev.writeCharacteristic(10, struct_left_speed)
        self.dev.writeCharacteristic(10, struct_tail)
        self.dev.writeCharacteristic(10, struct_zero)
        self.dev.writeCharacteristic(10, struct_zero)
        self.dev.writeCharacteristic(10, struct_zero)
        print(struct_left_direction, struct_left_speed)

        time.sleep(0.1)
        self.dev.writeCharacteristic(10, struct_header)
        self.dev.writeCharacteristic(10, struct_right)
        self.dev.writeCharacteristic(10, struct_right_direction)
        self.dev.writeCharacteristic(10, struct_right_speed)
        self.dev.writeCharacteristic(10, struct_tail)
        self.dev.writeCharacteristic(10, struct_zero)
        self.dev.writeCharacteristic(10, struct_zero)
        self.dev.writeCharacteristic(10, struct_zero)
        print(struct_right_direction, struct_right_speed)

if __name__ == '__main__':
    gui = GUI()
