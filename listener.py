
import serial
import time
import multiprocessing
import os

import threading

class Listener_Warning(multiprocessing.Process):
    SERIAL_BAUDRATE = 9600
    PATH_TO_COM     = "/dev/"
    
    
    
    def __init__(self, input_queue, output_queue):
        # self.output_img_queue  = output_img_queue
        # self.output_mark_queue = output_mark_queue
        # self.serv_time         = start_server_time
        # self.bin_parser        = bin_parser
        # self.dir_gps_port      = "/dev/pts/"
        # self.name_gps_port     = "3"
        multiprocessing.Process.__init__(self)
        
       
        
        files = os.listdir("/dev/")
        contr = list(filter(lambda x : x.find("ttyUSB") != -1, files))

        print(contr)
        if len(contr) != 0:
                        
            # dev = self.PATH_TO_COM + contr[0]
            self.ports = list(map(lambda x : self.PATH_TO_COM + contr[0] + x, contr))
            dev     = self.PATH_TO_COM + contr[0]
            self.sp = serial.Serial(dev, self.SERIAL_BAUDRATE, timeout=1)
            self.sp.flushInput()
            self.arduino_port_init = True
            self.output_queue      = output_queue
        # self.try_init_port()
        
    def run(self):
    
    # if self.sp != None:

        while True:
            # look for incoming tornado request
            # if not self.input_queue.empty():
            #     data = self.input_queue.get()

            #     # send it to the serial device
            #     self.writeSerial(data)
            #     print ("writing to serial: " + data)

            # look for incoming serial data
            if (self.sp.inWaiting() > 0):
                self.lock.acquire()
                data = self.readSerial()
                self.lock.release()
                print("procces")
                print(data)
                cmd = data.split(',')[0]
                if cmd == "warning":
                    self.output_queue.put("warning, test12")
                    # print("WARNING EPTA SYKA")