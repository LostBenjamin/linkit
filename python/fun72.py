#!/usr/bin/python


import serial 
import time
import random

s = None

inter_command_delay = 0.0

def command(cmd_text):                                                                   
  s.write((cmd_text + '|').encode())                                                     
  time.sleep(inter_command_delay)    

def setup(): 
  global s 
  s = serial.Serial("/dev/ttyS0", 57600) 
#  command("fade")
#  time.sleep(2)
  command("erase")
  time.sleep(0.1)

def run(): 
  while True:
    command("pause")

    for x in range(0, 4):
      command("blue|bright|bright|blinkr|repeat")
      command("white|bright|blinkr|repeat") 
      command("blue|bright|blinkr|repeat") 
      command("red|bright|blinkr|repeat") 

    command("mirror")
    command("continue")
    time.sleep(10.0)

if __name__ == '__main__': 
  setup()
  run() 
