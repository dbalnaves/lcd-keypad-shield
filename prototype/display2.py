#!/usr/bin/env python

import time, os

## Create a few strings for file I/O equivalence
HIGH = "1"
LOW =  "0"
INPUT = "0"
OUTPUT = "1"
INPUT_PU = "8"

BACKLIGHT = 3
RS = 8
EN = 9
D1 = 7
D2 = 6
D3 = 5
D4 = 4

## For simplicity's sake, we'll create a string for our paths.
GPIO_MODE_PATH= os.path.normpath('/sys/devices/virtual/misc/gpio/mode/')
GPIO_PIN_PATH=os.path.normpath('/sys/devices/virtual/misc/gpio/pin/')
GPIO_FILENAME="gpio"

## create a couple of empty arrays to store the pointers for our files
pinMode = []
pinData = []

## First, populate the arrays with file objects that we can use later.
for i in range(0,18):
  pinMode.append(os.path.join(GPIO_MODE_PATH, 'gpio'+str(i)))
  pinData.append(os.path.join(GPIO_PIN_PATH, 'gpio'+str(i)))

def digitalWrite(pin,mode):
  file = open(pinData[pin], 'r+')
  file.write(mode)
  file.close()
  return

def RS_L():
  digitalWrite(RS,LOW)
  return

def RS_H():
  digitalWrite(RS,HIGH)
  return

def EN_L():
  digitalWrite(EN,LOW)
  return

def EN_H():
  digitalWrite(EN,HIGH)
  return

def set_pinMode(pin,mode):
  file = open(pinMode[pin], 'r+')
  file.write(mode)
  file.close()
  return

def set_backlight(mode):
  set_pinMode(BACKLIGHT,OUTPUT)
  digitalWrite(BACKLIGHT,mode)
  return

def write_data(dat):
  RS_H()
  EN_L()
  print (dat)
  temp=ord(dat) & 0xf0
  for i in range(D1,(D4-1),-1):
    if(temp&0x80):
      digitalWrite(i,HIGH)
    else:
      digitalWrite(i,LOW)
    temp <<= 1
  EN_H()
  time.sleep(1/10)
  EN_L()
  temp=(ord(dat) & 0x0f)<<4
  for i in range(D1,(D4-1),-1):
    if(temp&0x80):
      digitalWrite(i,HIGH)
    else:
      digitalWrite(i,LOW)
    temp <<= 1

  EN_H()
  time.sleep(1/10)
  EN_L()

def LCD_write_char(x,y,dat):
  if (x ==0):
   address = 0x80 + y
  else:
    address = 0xC0 + y
  
  write_command(address);
  print("address",address)
  write_data(dat);
  time.sleep(1/10)

def write_command(command):
  temp=command & 0xf0
  RS_L()
  EN_L()

  for i in range(D1,(D4-1),-1):
    print(i,temp&0x80,command)
    if(temp&0x80):
      digitalWrite(i,HIGH)
    else:
      digitalWrite(i,LOW)
    temp <<= 1

  EN_H()
  time.sleep(1/10)
  EN_L()

  temp=(command & 0x0f)<<4

  for i in range(D1,(D4-1),-1):
    print(i,temp&0x80,command)
    if(temp&0x80):
      digitalWrite(i,HIGH)
    else:
      digitalWrite(i,LOW)
    temp <<= 1

  EN_H()
  time.sleep(1/10)
  EN_L()
  return

def lcd1602_init():
  print("init")
  set_pinMode(RS,OUTPUT)
  set_pinMode(EN,OUTPUT)
  for i in range(D1,(D4-1),-1):
    set_pinMode(i,OUTPUT)
 
  write_command(0x33)
  write_command(0x32)
 
  time.sleep(100/1000)
  write_command(0x28)
  time.sleep(50/1000)
  write_command(0x06)
  time.sleep(50/1000)
  write_command(0x0c)
  time.sleep(50/1000)
  write_command(0x80)
  time.sleep(50/1000)
  write_command(0x01)
  time.sleep(100/1000)

set_backlight(HIGH)
lcd1602_init()
t_end = time.time() + 3
while time.time() < t_end:
  LCD_write_char(0,2,'W');
  LCD_write_char(0,3,'e');
  LCD_write_char(0,4,'l');
  LCD_write_char(0,5,'c');
  LCD_write_char(0,6,'o');
  LCD_write_char(0,7,'m');
  LCD_write_char(0,8,'e');

  LCD_write_char(0,10,'t');
  LCD_write_char(0,11,'o');

  LCD_write_char(1,4,'p');
  LCD_write_char(1,5,'c');
  LCD_write_char(1,6,'D');
  LCD_write_char(1,7,'u');
  LCD_write_char(1,8,'i');
  LCD_write_char(1,9,'n');
  LCD_write_char(1,10,'o');

write_command(0x01)
set_backlight(LOW)
