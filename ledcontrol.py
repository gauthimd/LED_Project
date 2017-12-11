#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_PCA9685  #module for PWM driver board
import time, random, lirc, threading, Queue, json, os, sys
from colors import Color
from LED import LED

pwm = Adafruit_PCA9685.PCA9685() #init for PWM driver
pwm.set_pwm_freq(200)
sockid = lirc.init("myprog", blocking=False) #init for LIRC socket

red = Color(255,0,0) #instantiate color objects from colors.py
green = Color(0,255,0)
blue = Color(0,0,255)
yellow = Color(215,200,0)
orange = Color(255,50,0)
turquoise = Color(0,255,255)
purple = Color(255,0,255)
gray = Color(100,100,100)
white = Color(255,255,255)

led1 = LED(0,1,2) #instantiate 3 LED objects for this 3 LED system
led2 = LED(3,4,5) #LED(R,G,B) = PWM board pin numbers
led3 = LED(6,7,8)

t = [led1, led2, led3] #list used to cycle through for modes

class System():

  def __init__(self):
      self.bright = 1
      self.delay = .5
      self.mode = 'Ok'
      self.modenum = 0
      self.args = None

  def turnon(self, color):
    for x in t:
      pwm.set_pwm(x.redpin, 0, int(color.redpwm*self.bright))
      pwm.set_pwm(x.greenpin, 0, int(color.greenpwm*self.bright))
      pwm.set_pwm(x.bluepin, 0, int(color.bluepwm*self.bright))
      x.redpwm = int(color.redpwm*self.bright)
      x.greenpwm = int(color.greenpwm*self.bright)
      x.bluepwm = int(color.bluepwm*self.bright)

  def turnon3separate(self, color1, color2, color3): 
      pwm.set_pwm(t[0].redpin, 0, int(color1.redpwm*self.bright))
      pwm.set_pwm(t[0].greenpin, 0, int(color1.greenpwm*self.bright))
      pwm.set_pwm(t[0].bluepin, 0, int(color1.bluepwm*self.bright))
      t[0].redpwm = int(color1.redpwm*self.bright)
      t[0].greenpwm = int(color1.greenpwm*self.bright)
      t[0].bluepwm = int(color1.bluepwm*self.bright)
      pwm.set_pwm(t[1].redpin, 0, int(color2.redpwm*self.bright))
      pwm.set_pwm(t[1].greenpin, 0, int(color2.greenpwm*self.bright))
      pwm.set_pwm(t[1].bluepin, 0, int(color2.bluepwm*self.bright))
      t[1].redpwm = int(color2.redpwm*self.bright)
      t[1].greenpwm = int(color2.greenpwm*self.bright)
      t[1].bluepwm = int(color2.bluepwm*self.bright)
      pwm.set_pwm(t[2].redpin, 0, int(color3.redpwm*self.bright))
      pwm.set_pwm(t[2].greenpin, 0, int(color3.greenpwm*self.bright))
      pwm.set_pwm(t[2].bluepin, 0, int(color3.bluepwm*self.bright))
      t[2].redpwm = int(color3.redpwm*self.bright)
      t[2].greenpwm = int(color3.greenpwm*self.bright)
      t[2].bluepwm = int(color3.bluepwm*self.bright)

  def turnoff(self):
    for x in t:
      pwm.set_pwm(x.redpin, 0, 0)
      pwm.set_pwm(x.greenpin, 0, 0)
      pwm.set_pwm(x.bluepin, 0, 0)
      x.redpwm = 0
      x.greenpwm = 0
      x.bluepwm = 0

  def fadeoff(self):
    u = []
    for x in t:
      limit = max(x.redpwm, x.greenpwm, x.bluepwm)
      u.append(limit)
    limit = max(u)
    for i in range(limit/100):
      for x in t:
        if 100*i <= x.redpwm:
          pwm.set_pwm(x.redpin, 0, x.redpwm - 100*i)
        else:
          pwm.set_pwm(x.redpin, 0, 0) 
        if 100*i <= x.greenpwm:
          pwm.set_pwm(x.greenpin, 0, x.greenpwm - 100*i)
        else:
          pwm.set_pwm(x.greenpin, 0, 0) 
        if 100*i <= x.bluepwm:
          pwm.set_pwm(x.bluepin, 0, x.bluepwm - 100*i)
        else:
          pwm.set_pwm(x.bluepin, 0, 0) 
      time.sleep(.001)
    for x in t:
      pwm.set_pwm(x.redpin, 0, 0)
      pwm.set_pwm(x.greenpin, 0, 0)
      pwm.set_pwm(x.bluepin, 0, 0)  
      x.redpwm = 0
      x.greenpwm = 0
      x.bluepwm = 0

  def shift(self, tocolor):
    u = []
    for x in t:
      maxdiff = max(abs(x.redpwm - tocolor.redpwm*self.bright), abs(x.greenpwm - tocolor.greenpwm*self.bright), abs(x.bluepwm - tocolor.bluepwm*self.bright))
      x.reddiff = abs(x.redpwm - tocolor.redpwm*self.bright)
      x.greendiff = abs(x.greenpwm - tocolor.greenpwm*self.bright)
      x.bluediff = abs(x.bluepwm - tocolor.bluepwm*self.bright)
      u.append(maxdiff)
    maxdiff = max(u)
    for i in range(int(maxdiff/100)):
      for x in t:
        if 100*i <= x.reddiff:
          if x.redpwm < tocolor.redpwm*self.bright:
            pwm.set_pwm(x.redpin, 0, x.redpwm + 100*i)
          elif x.redpwm > tocolor.redpwm*self.bright:
            pwm.set_pwm(x.redpin, 0, x.redpwm - 100*i)
        else:
          pwm.set_pwm(x.redpin, 0, int(tocolor.redpwm*self.bright))
        if 100*i <= x.greendiff:
          if x.greenpwm < tocolor.greenpwm*self.bright:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm + 100*i)
          elif x.greenpwm > tocolor.greenpwm*self.bright:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm - 100*i)
        else:
          pwm.set_pwm(x.greenpin, 0, int(tocolor.greenpwm*self.bright))
        if 100*i <= x.bluediff:
          if x.bluepwm < tocolor.bluepwm*self.bright:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm + 100*i)
          elif x.bluepwm > tocolor.bluepwm*self.bright:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm - 100*i)
        else:
          pwm.set_pwm(x.bluepin, 0, int(tocolor.bluepwm*self.bright))
    for x in t:
      pwm.set_pwm(x.redpin, 0, int(tocolor.redpwm*self.bright))
      pwm.set_pwm(x.greenpin, 0, int(tocolor.greenpwm*self.bright))
      pwm.set_pwm(x.bluepin, 0, int(tocolor.bluepwm*self.bright))
      x.redpwm = int(tocolor.redpwm*self.bright)
      x.greenpwm = int(tocolor.greenpwm*self.bright)
      x.bluepwm = int(tocolor.bluepwm*self.bright)

  def siren(self):
    self.mode = self.siren
    self.args = 'None'
    delay = 1.85*self.delay+.15 #puts delay btwn .33sec and 2 sec
    initim = time.time()
    then = initim + delay
    colors = {1:red,2:blue}
    th = threading.currentThread()
    y = 1
    self.turnoff()
    self.turnon(colors[y])
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        y += 1
        if y == 3: y = 1
        self.turnoff()
        self.turnon(colors[y])
        then = now + delay
      time.sleep(.001)

  def cyclecolors(self):
    self.mode = self.cyclecolors
    self.args = 'None'
    th = threading.currentThread()
    initim = time.time()
    then = initim + self.delay
    colors = {1:red,2:orange,3:yellow,4:green,5:blue,6:turquoise,7:purple,8:white}
    y = 1
    self.turnoff()
    self.turnon(colors[y])
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        y +=1
        if y==9: y=1
        self.turnon(colors[y])
        then = now + self.delay
      time.sleep(.001)

  def valentines(self):
    self.mode = self.valentines
    self.args = 'None'
    ldelay = 1.25
    sdelay = .15
    n = 1
    th = threading.currentThread()
    initim = time.time()
    then = initim + ldelay
    self.turnoff()
    for x in t:
      pwm.set_pwm(x.redpin, 0, int(2000*self.bright))
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        if n % 2 != 0:
          for x in t:
            pwm.set_pwm(x.redpin, 0, int(4000*self.bright))
          n += 1
          if n > 4:
            n = 1
            then = now + ldelay
          else:
            then = now + sdelay
        else:
          for x in t:
            pwm.set_pwm(x.redpin, 0, int(2000*self.bright))
          then = now + sdelay
          n += 1
      else: time.sleep(.001)
    self.turnoff()

  def holidays(self, d):
    self.mode = self.holidays
    self.args = d
    th = threading.currentThread()
    x = 0
    y = 1
    z = 2
    initim = time.time()
    then = initim + self.delay
    self.turnoff()
    self.turnon3separate(d[y],d[x],d[z])
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
          self.turnon3separate(d[y],d[x],d[z])
          x += 1
          if x >= len(d): x = 0
          y += 1
          if y >= len(d): y = 0
          z += 1
          if z >= len(d): z = 0
          then = now + self.delay
      else: time.sleep(.001)
    self.turnoff()

  def randomsync(self):
    self.mode = self.randomsync
    self.args = 'None'
    th = threading.currentThread()
    then = time.time() + 5
    d = {1:red,2:green,3:blue,4:turquoise,5:purple,6:orange,7:yellow,8:white}
    y = random.randint(1,8)
    self.shift(d[y])
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        y = random.randint(1,8)
        self.shift(d[y])
        then = now + random.randint(5,30)
      else:
        time.sleep(.001)
    self.turnoff()

  def randomasync(self):
    self.mode = self.randomasync
    self.args = 'None'
    th = threading.currentThread()
    then = time.time() + 5
    d = {1:red,2:green,3:blue,4:turquoise,5:purple,6:orange,7:yellow,8:white}
    x = random.randint(1,8)
    y = random.randint(1,8)
    z = random.randint(1,8)
    self.turnoff()
    self.turnon3separate(d[x],d[y],d[z])
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        x = random.randint(1,8)
        y = random.randint(1,8)
        z = random.randint(1,8)
        self.turnon3separate(d[x],d[y],d[z])
        then = now + random.randint(5,30)
      else:
        time.sleep(.001)
    self.turnoff()

  def randcolor(self):
    x = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return x

  def brightnessup(self):
    if self.bright > .95: pass
    else: self.bright += 0.1
    print "Brightness ", self.bright*100, "%"

  def brightnessdown(self):
    if self.bright < 0.15: pass
    else: self.bright -= 0.1
    print "Brightness ", self.bright*100, "%"

  def speeddown(self):
    if self.delay > .95: pass
    else: self.delay += 0.1
    print "Delay", self.delay*100,"%"

  def speedup(self):
    if self.delay < 0.15: pass
    else: self.delay -= 0.1
    print "Delay", self.delay*100,"%"

  def modedown(self, m):
    self.modenum -= 1
    if self.modenum < 1: self.modenum = len(m)

  def modeup(self, m):
    self.modenum += 1
    if self.modenum > len(m): self.modenum = 1

  def checkcodes(self, q):
    th = threading.currentThread()
    while getattr(th, "do_run", True):
      try:
        x = lirc.nextcode()
        y = ""
        for n in x:
          y = x[0].encode('utf-8')
        q.put(y)
        time.sleep(.1)
      except KeyboardInterrupt: break

  def checkcodes2(self, q):
    th = threading.currentThread()
    while getattr(th, "do_run", True):
      try:
        if os.path.exists('/home/pi/LED_Project/input.json'):
          with open('/home/pi/LED_Project/input.json') as infile:
            print infile.read
            data = json.load(infile)
            print data
          if data.get("input"):
            y = data["input"]
            y = y.encode('utf-8')
            q.put(y)
            print "added to q", y
            os.remove('/home/pi/LED_Project/input.json')
            print "removed"
        time.sleep(.1)
      except KeyboardInterrupt: pass 

  def run(self):
    d = {'1':self.shift,'2':self.shift,'3':self.shift,'4':self.shift,
         '5':self.shift,'6':self.shift,'7':self.shift,
         'Ok':self.fadeoff,'0':self.shift,'Star':self.brightnessdown,
         'Pound':self.brightnessup,'Left':self.speeddown,
         'Right':self.speedup,'Up':self.modeup,'Down':self.modedown}
    d2 = {'1':red,'2':green,'3':blue,'4':orange,'5':turquoise,'6':purple,
          '7':yellow,'0':white}
    m = {1:self.siren,2:self.cyclecolors,3:self.valentines,4:self.holidays,5:self.holidays,
         6:self.randomsync,7:self.randomasync,8:self.holidays}
    m2 = {4:{0:red,1:white,2:blue},5:{0:red,1:green,2:white},8:{0:red,1:orange,2:yellow,3:green,4:turquoise,5:blue,6:purple,7:white}}
    q = Queue.Queue()
    t1 = threading.Thread(target=self.checkcodes,args=(q,))
    t1.daemon = True
    t1.start()
    t3 = threading.Thread(target=self.checkcodes2,args=(q,))
    t3.daemon = True
    t3.start()
    while True:
      try:
        y = q.get()
        if len(y) > 0:
          if y in d:
            try:
              t2.do_run = False
            except: pass
            if y in d2:
              t2 = threading.Thread(target=d[y],args=(d2[y],))
              t2.daemon = True
              t2.start()
              self.mode = d[y]
              self.args = d2[y]
            elif y == 'Star' or y == 'Pound' or y == 'Left' or y == 'Right':
              if y == 'Star': self.brightnessdown()
              if y == 'Pound': self.brightnessup()
              if y == 'Left': self.speeddown()
              if y == 'Right': self.speedup()
              if self.args == 'None':
                t2 = threading.Thread(target=self.mode) 
              else:
                t2 = threading.Thread(target=self.mode,args=(self.args,)) 
              t2.daemon = True
              t2.start()
            elif y == 'Up':
              self.modeup(m)
	      if self.modenum in m2:
                t2 = threading.Thread(target=m[self.modenum],args=(m2[self.modenum],)) 
              else:
                t2 = threading.Thread(target=m[self.modenum]) 
              t2.daemon = True
              t2.start()
            elif y == 'Down':
              self.modedown(m)
              if self.modenum in m2:
                t2 = threading.Thread(target=m[self.modenum],args=(m2[self.modenum],))
              else:
                t2 = threading.Thread(target=m[self.modenum]) 
              t2.daemon = True
              t2.start()
            else:
              t2 = threading.Thread(target=d[y])
              t2.daemon = True
              t2.start()
              self.mode = d[y]
              self.args = 'None'
        time.sleep(.1)
      except KeyboardInterrupt:
        print "\nYou pressed Ctrl+C or somethin fucked up"
        break
    try:
      t1.do_run = False
      t1.join()
      t2.do_run = False
      t2.join()
      t3.do_run = False
      t3.join()
    except: pass

if __name__=="__main__":
  sys = System() #create object
  sys.turnon(green) #blink green twice to show ready
  time.sleep(.25)
  sys.turnoff()
  time.sleep(.25)
  sys.turnon(green)
  time.sleep(.25)
  sys.turnoff()
  sys.run() #start main program
  sys.turnoff() #turn shit off
  print "Done"
