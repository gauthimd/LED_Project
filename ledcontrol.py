#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_PCA9685
import time, random, lirc, signal, threading, Queue

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(200)
sockid = lirc.init("myprog", blocking=False)

class Color():

  def __init__(self, red, green, blue):
    self.redpwm = int(red*16.059)   #Convert 8 bits to 12 bits 
    self.greenpwm = int(green*16.059)   
    self.bluepwm = int(blue*16.059)

red = Color(255,0,0)
green = Color(0,255,0)
blue = Color(0,0,255)
yellow = Color(215,200,0)
orange = Color(255,50,0)
turquoise = Color(0,255,255)
purple = Color(255,0,255)
gray = Color(100,100,100)
white = Color(255,255,255)

class LED():

  def __init__(self, redpin, greenpin, bluepin):
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(100)
    self.redpin = redpin
    self.greenpin = greenpin
    self.bluepin = bluepin
    self.redpwm = 0
    self.greenpwm = 0
    self.bluepwm = 0

  def turnon(self, color):
    pwm.set_pwm(self.redpin, 0, color.redpwm)
    pwm.set_pwm(self.greenpin, 0, color.greenpwm)
    pwm.set_pwm(self.bluepin, 0, color.bluepwm)
    self.redpwm = color.redpwm
    self.greenpwm = color.greenpwm
    self.bluepwm = color.bluepwm

  def turnoff(self):
    pwm.set_pwm(self.redpin, 0, 0)
    pwm.set_pwm(self.greenpin, 0, 0)
    pwm.set_pwm(self.bluepin, 0, 0)
    self.redpwm = 0
    self.greenpwm = 0
    self.bluepwm = 0

  def fadeon(self, color):
    limit = max(color.redpwm, color.greenpwm, color.bluepwm)
    for i in range(limit/100):
      if 100*i <= color.redpwm:
        pwm.set_pwm(self.redpin, 0, 100*i)
      else:
        pwm.set_pwm(self.redpin, 0, color.redpwm) 
      if 100*i <= color.greenpwm:
        pwm.set_pwm(self.greenpin, 0, 100*i)
      else:
        pwm.set_pwm(self.greenpin, 0, color.greenpwm) 
      if 100*i <= color.bluepwm:
        pwm.set_pwm(self.bluepin, 0, 100*i)
      else:
        pwm.set_pwm(self.bluepin, 0, color.bluepwm) 
      time.sleep(.001)
    pwm.set_pwm(self.redpin, 0, color.redpwm)
    pwm.set_pwm(self.greenpin, 0, color.greenpwm)
    pwm.set_pwm(self.bluepin, 0, color.bluepwm)   
    self.redpwm = color.redpwm
    self.greenpwm = color.greenpwm
    self.bluepwm = color.bluepwm

  def fadeoff(self):
    limit = max(self.redpwm, self.greenpwm, self.bluepwm)
    for i in range(limit/100):
      if 100*i <= self.redpwm:
        pwm.set_pwm(self.redpin, 0, self.redpwm - 100*i)
      else:
        pwm.set_pwm(self.redpin, 0, 0) 
      if 100*i <= self.greenpwm:
        pwm.set_pwm(self.greenpin, 0, self.greenpwm - 100*i)
      else:
        pwm.set_pwm(self.greenpin, 0, 0) 
      if 100*i <= self.bluepwm:
        pwm.set_pwm(self.bluepin, 0, self.bluepwm - 100*i)
      else:
        pwm.set_pwm(self.bluepin, 0, 0) 
      time.sleep(.001)
    pwm.set_pwm(self.redpin, 0, 0)
    pwm.set_pwm(self.greenpin, 0, 0)
    pwm.set_pwm(self.bluepin, 0, 0)  
    self.redpwm = 0
    self.greenpwm = 0
    self.bluepwm = 0

  def fadeonoff(self, color):
    limit = max(color.redpwm, color.greenpwm, color.bluepwm)
    for i in range(limit/10):
      if 10*i <= color.redpwm:
        pwm.set_pwm(self.redpin, 0, 10*i)
      else: pwm.set_pwm(self.redpin, 0, color.redpwm)
      if 10*i <= color.greenpwm:
        pwm.set_pwm(self.greenpin, 0, 10*i)
      else: pwm.set_pwm(self.greenpin, 0, color.greenpwm)
      if 10*i <= color.bluepwm:
        pwm.set_pwm(self.bluepin, 0, 10*i)
      else: pwm.set_pwm(self.bluepin, 0, color.bluepwm)
    self.redpwm = color.redpwm
    self.greenpwm = color.greenpwm
    self.bluepwm = color.bluepwm
    for i in range(limit/10):
      if 10*i <= color.redpwm:
        pwm.set_pwm(self.redpin, 0, color.redpwm - 10*i)
      else: pwm.set_pwm(self.redpin, 0, 0)
      if 10*i <= color.greenpwm:
        pwm.set_pwm(self.greenpin, 0, color.greenpwm - 10*i)
      else: pwm.set_pwm(self.greenpin, 0, 0)
      if 10*i <= color.bluepwm:
        pwm.set_pwm(self.bluepin, 0, color.bluepwm - 10*i)
      else: pwm.set_pwm(self.bluepin, 0, 0)
    pwm.set_pwm(self.redpin, 0, 0)
    pwm.set_pwm(self.greenpin, 0, 0)
    pwm.set_pwm(self.bluepin, 0, 0)
    self.redpwm = 0
    self.greenpwm = 0
    self.bluepwm = 0

  def blink(self, color):
    blinkspeed = .05
    for x in range(20):
      self.turnon(color)
      time.sleep(blinkspeed)
      self.turnoff()
      time.sleep(blinkspeed)

  def siren(self):
    for i in range(10):
      self.turnon(red)
      time.sleep(.25)
      self.turnoff()
      self.turnon(blue)
      time.sleep(.25)
      self.turnoff()

  def shift(self, tocolor):
    maxdiff = max(abs(self.redpwm - tocolor.redpwm), abs(self.greenpwm - tocolor.greenpwm), abs(self.bluepwm - tocolor.bluepwm))
    reddiff = abs(self.redpwm - tocolor.redpwm)
    greendiff = abs(self.greenpwm - tocolor.greenpwm)
    bluediff = abs(self.bluepwm - tocolor.bluepwm)
    for i in range(maxdiff/10):
      if 10*i <= reddiff:
        if self.redpwm < tocolor.redpwm:
          pwm.set_pwm(self.redpin, 0, self.redpwm + 10*i)
        elif self.redpwm > tocolor.redpwm:
          pwm.set_pwm(self.redpin, 0, self.redpwm - 10*i)
      else:
        pwm.set_pwm(self.redpin, 0, tocolor.redpwm)
      if 10*i <= greendiff:
        if self.greenpwm < tocolor.greenpwm:
          pwm.set_pwm(self.greenpin, 0, self.greenpwm + 10*i)
        elif self.greenpwm > tocolor.greenpwm:
          pwm.set_pwm(self.greenpin, 0, self.greenpwm - 10*i)
      else:
        pwm.set_pwm(self.greenpin, 0, tocolor.greenpwm)
      if 10*i <= bluediff:
        if self.bluepwm < tocolor.bluepwm:
          pwm.set_pwm(self.bluepin, 0, self.bluepwm + 10*i)
        elif self.bluepwm > tocolor.bluepwm:
          pwm.set_pwm(self.bluepin, 0, self.bluepwm - 10*i)
      else:
        pwm.set_pwm(self.bluepin, 0, tocolor.bluepwm)
    pwm.set_pwm(self.redpin, 0, tocolor.redpwm)
    pwm.set_pwm(self.greenpin, 0, tocolor.greenpwm)
    pwm.set_pwm(self.bluepin, 0, tocolor.bluepwm)
    self.redpwm = tocolor.redpwm
    self.greenpwm = tocolor.greenpwm
    self.bluepwm = tocolor.bluepwm

  def slowshift(self, fromcolor, tocolor):
    maxdiff = max(abs(fromcolor.redpwm - tocolor.redpwm), abs(fromcolor.greenpwm - tocolor.greenpwm), abs(fromcolor.bluepwm - tocolor.bluepwm))
    reddiff = abs(fromcolor.redpwm - tocolor.redpwm)
    greendiff = abs(fromcolor.greenpwm - tocolor.greenpwm)
    bluediff = abs(fromcolor.bluepwm - tocolor.bluepwm)
    for i in range(maxdiff):
      if i <= reddiff:
        if fromcolor.redpwm < tocolor.redpwm:
          pwm.set_pwm(self.redpin, 0, fromcolor.redpwm + i)
        elif fromcolor.redpwm > tocolor.redpwm:
          pwm.set_pwm(self.redpin, 0, fromcolor.redpwm - i)
      else:
        pwm.set_pwm(self.redpin, 0, tocolor.redpwm)
      if i <= greendiff:
        if fromcolor.greenpwm < tocolor.greenpwm:
          pwm.set_pwm(self.greenpin, 0, fromcolor.greenpwm + i)
        elif fromcolor.greenpwm > tocolor.greenpwm:
          pwm.set_pwm(self.greenpin, 0, fromcolor.greenpwm - i)
      else:
        pwm.set_pwm(self.greenpin, 0, tocolor.greenpwm)
      if i <= bluediff:
        if fromcolor.bluepwm < tocolor.bluepwm:
          pwm.set_pwm(self.bluepin, 0, fromcolor.bluepwm + i)
        elif fromcolor.bluepwm > tocolor.bluepwm:
          pwm.set_pwm(self.bluepin, 0, fromcolor.bluepwm - i)
      else:
        pwm.set_pwm(self.bluepin, 0, tocolor.bluepwm)
    pwm.set_pwm(self.redpin, 0, tocolor.redpwm)
    pwm.set_pwm(self.greenpin, 0, tocolor.greenpwm)
    pwm.set_pwm(self.bluepin, 0, tocolor.bluepwm)

  def randcolor(self):
    x = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return x

  def randcoolcolor(self):
    x = Color(0,random.randint(0,255),random.randint(0,255))
    return x

  def randwarmcolor(self):
    x = Color(random.randint(55,255),random.randint(0,225),0)
    return x

  def randshifter(self):
    i = self.randcolor()
    j = self.randcolor()
    self.fadeon(i)
    time.sleep(2)
    for x in range(10):
      self.shift(i,j)
      time.sleep(1)
      i = j
      j = self.randcoolcolor()
    self.fadeoff(i)

  def randcoolshifter(self):
    i = self.randcoolcolor()
    j = self.randcoolcolor()
    self.fadeon(i)
    time.sleep(2)
    for x in range(5):
      self.shift(i,j)
      time.sleep(random.randint(1,5))
      i = j
      j = self.randcoolcolor()
    self.fadeoff(i)
  
  def fireplace(self):
    for x in range(100):
      i = self.randwarmcolor()
      self.turnoff()
      self.turnon(i)
      time.sleep(.025)
    self.turnoff()

  def cyclecolors(self, cyctime):
    self.turnon(red)
    time.sleep(cyctime)
    self.turnon(orange)
    time.sleep(cyctime)
    self.turnon(yellow)
    time.sleep(cyctime)
    self.turnon(green)
    time.sleep(cyctime)
    self.turnon(blue)
    time.sleep(cyctime)
    self.turnon(turquoise)
    time.sleep(cyctime)
    self.turnon(purple)
    time.sleep(cyctime)
    self.turnon(white)
    time.sleep(cyctime)
    self.turnoff()

  def rainbowshift(self):
    self.fadeon(red)
    self.shift(red,orange)
    self.shift(orange, yellow)
    self.shift(yellow, green)
    self.shift(green, turquoise)
    self.shift(turquoise, blue)
    self.shift(blue, purple)
    self.shift(purple, white)
    time.sleep(1)
    self.fadeoff(white)

class System():
  led1 = LED(0,1,2)
  led2 = LED(3,4,5)
  led3 = LED(6,7,8)
  global t
  t = [led1, led2, led3]

  def turnon(self, color):
    for x in t:
      pwm.set_pwm(x.redpin, 0, color.redpwm)
      pwm.set_pwm(x.greenpin, 0, color.greenpwm)
      pwm.set_pwm(x.bluepin, 0, color.bluepwm)
      x.redpwm = color.redpwm
      x.greenpwm = color.greenpwm
      x.bluepwm = color.bluepwm

  def turnoff(self):
    for x in t:
      pwm.set_pwm(x.redpin, 0, 0)
      pwm.set_pwm(x.greenpin, 0, 0)
      pwm.set_pwm(x.bluepin, 0, 0)
      x.redpwm = 0
      x.greenpwm = 0
      x.bluepwm = 0

  def fadeon(self, color):
    limit = max(color.redpwm, color.greenpwm, color.bluepwm)
    for i in range(limit/100):
      for x in t:
        if 100*i <= color.redpwm:
          pwm.set_pwm(x.redpin, 0, 100*i)
        else:
          pwm.set_pwm(x.redpin, 0, color.redpwm) 
        if 100*i <= color.greenpwm:
          pwm.set_pwm(x.greenpin, 0, 100*i)
        else:
          pwm.set_pwm(x.greenpin, 0, color.greenpwm) 
        if 100*i <= color.bluepwm:
          pwm.set_pwm(x.bluepin, 0, 100*i)
        else:
          pwm.set_pwm(x.bluepin, 0, color.bluepwm) 
      time.sleep(.001)
    for x in t:
      pwm.set_pwm(x.redpin, 0, color.redpwm)
      pwm.set_pwm(x.greenpin, 0, color.greenpwm)
      pwm.set_pwm(x.bluepin, 0, color.bluepwm)   
      x.redpwm = color.redpwm
      x.greenpwm = color.greenpwm
      x.bluepwm = color.bluepwm

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

  def siren(self):
    initim = time.time()
    delay = .25
    then = initim + delay
    colors = {1:red,2:blue}
    th = threading.currentThread()
    y = 1
    for x in t:
      x.turnon(colors[y])
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        y += 1
        if y == 3: y = 1
        for x in t:
          x.turnoff()
          x.turnon(colors[y])
          then = now + delay
      time.sleep(.001)
    for x in t:
      x.turnoff()

  def shift(self, tocolor):
    u = []
    for x in t:
      maxdiff = max(abs(x.redpwm - tocolor.redpwm), abs(x.greenpwm - tocolor.greenpwm), abs(x.bluepwm - tocolor.bluepwm))
      x.reddiff = abs(x.redpwm - tocolor.redpwm)
      x.greendiff = abs(x.greenpwm - tocolor.greenpwm)
      x.bluediff = abs(x.bluepwm - tocolor.bluepwm)
      u.append(maxdiff)
    maxdiff = max(u)
    for i in range(maxdiff/100):
      for x in t:
        if 100*i <= x.reddiff:
          if x.redpwm < tocolor.redpwm:
            pwm.set_pwm(x.redpin, 0, x.redpwm + 100*i)
          elif x.redpwm > tocolor.redpwm:
            pwm.set_pwm(x.redpin, 0, x.redpwm - 100*i)
        else:
          pwm.set_pwm(x.redpin, 0, tocolor.redpwm)
        if 100*i <= x.greendiff:
          if x.greenpwm < tocolor.greenpwm:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm + 100*i)
          elif x.greenpwm > tocolor.greenpwm:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm - 100*i)
        else:
          pwm.set_pwm(x.greenpin, 0, tocolor.greenpwm)
        if 100*i <= x.bluediff:
          if x.bluepwm < tocolor.bluepwm:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm + 100*i)
          elif x.bluepwm > tocolor.bluepwm:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm - 100*i)
        else:
          pwm.set_pwm(x.bluepin, 0, tocolor.bluepwm)
    for x in t:
      pwm.set_pwm(x.redpin, 0, tocolor.redpwm)
      pwm.set_pwm(x.greenpin, 0, tocolor.greenpwm)
      pwm.set_pwm(x.bluepin, 0, tocolor.bluepwm)
      x.redpwm = tocolor.redpwm
      x.greenpwm = tocolor.greenpwm
      x.bluepwm = tocolor.bluepwm

  def cyclecolors(self):
    colors = {1:red,2:orange,3:yellow,4:green,5:blue,6:turquoise,7:purple,8:white}
    th = threading.currentThread()
    y = 1
    initim = time.time()
    delay = .25
    then = initim + delay
    for x in t:
      x.turnon(colors[y])
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        y +=1
        if y==9: y=1
        for x in t:
          x.turnon(colors[y])
        then = now + delay
      time.sleep(.001)
    for x in t:
      x.turnoff()

  def valentines(self):
    self.turnoff()
    for r in range(10):
      for x in t:
        pwm.set_pwm(x.redpin, 0, 2000)
      time.sleep(1)
      for x in t:
        pwm.set_pwm(x.redpin, 0, 4000)
      time.sleep(.05)
      for x in t:
        pwm.set_pwm(x.redpin, 0, 2000)
      time.sleep(.05)
      for x in t:
        pwm.set_pwm(x.redpin, 0, 4000)
      time.sleep(.05)
      for x in t:
        pwm.set_pwm(x.redpin, 0, 2000)

  def fourthofjulyfade(self):
    self.turnoff()
    boo = 1 
    for r in range(5):
      if boo == 4: boo = 1
      if boo == 1: d = {1:red, 2:white, 3:blue}
      elif boo == 2: d = {1:white, 2:blue, 3:red}
      elif boo == 3: d = {1:blue, 2:red, 3:white}
      u = []
      n = 1
      for x in t:
        if n > len(d): n = 1
        maxdiff = max(abs(x.redpwm - d[n].redpwm), abs(x.greenpwm - d[n].greenpwm), abs(x.bluepwm - d[n].bluepwm))
        x.reddiff = abs(x.redpwm - d[n].redpwm)
        x.greendiff = abs(x.greenpwm - d[n].greenpwm)
        x.bluediff = abs(x.bluepwm - d[n].bluepwm)
        u.append(maxdiff)
        n += 1
      maxdiff = max(u)
      for i in range(maxdiff/100):
        n = 1
        for x in t:
          if n > len(d): n = 1
          if 100*i <= x.reddiff:
            if x.redpwm < d[n].redpwm:
              pwm.set_pwm(x.redpin, 0, x.redpwm + 100*i)
            elif x.redpwm > d[n].redpwm:
              pwm.set_pwm(x.redpin, 0, x.redpwm - 100*i)
          else:
            pwm.set_pwm(x.redpin, 0, d[n].redpwm)
          if 100*i <= x.greendiff:
            if x.greenpwm < d[n].greenpwm:
              pwm.set_pwm(x.greenpin, 0, x.greenpwm + 100*i)
            elif x.greenpwm > d[n].greenpwm:
              pwm.set_pwm(x.greenpin, 0, x.greenpwm - 100*i)
          else:
            pwm.set_pwm(x.greenpin, 0, d[n].greenpwm)
          if 100*i <= x.bluediff:
            if x.bluepwm < d[n].bluepwm:
              pwm.set_pwm(x.bluepin, 0, x.bluepwm + 100*i)
            elif x.bluepwm > d[n].bluepwm:
              pwm.set_pwm(x.bluepin, 0, x.bluepwm - 100*i)
          else:
            pwm.set_pwm(x.bluepin, 0, d[n].bluepwm)
          n += 1
      n = 1
      for x in t:
        if n > len(d): n = 1
        x.redpwm = d[n].redpwm
        x.greenpwm = d[n].greenpwm
        x.bluepwm = d[n].bluepwm
        n += 1
      boo += 1
      time.sleep(1)

  def fourthofjuly(self):
    self.turnoff()
    boo = 1 
    for r in range(5):
      if boo == 4: boo = 1
      if boo == 1: d = {1:red, 2:white, 3:blue}
      elif boo == 2: d = {1:white, 2:blue, 3:red}
      elif boo == 3: d = {1:blue, 2:red, 3:white}
      n = 1
      for x in t:
        if n > len(d): n = 1
        x.turnon(d[n])
        n += 1
      boo += 1
      time.sleep(.25)

  def christmas(self):
    self.turnoff()
    boo = 1 
    for r in range(5):
      if boo == 3: boo = 1
      if boo == 1: d = {1:red, 2:green}
      elif boo == 2: d = {1:green, 2:red}
      n = 1
      for x in t:
        if n > len(d): n = 1
        x.turnon(d[n])
        n += 1
      boo += 1
      time.sleep(.5)

  def christmasfade(self):
    self.turnoff()
    boo = False
    for r in range(5):
      if boo == False: d = {1:red, 2:green}
      else: d = {1:green, 2:red}
      u = []
      n = 1
      for x in t:
        if n > len(d): n = 1
        maxdiff = max(abs(x.redpwm - d[n].redpwm), abs(x.greenpwm - d[n].greenpwm), abs(x.bluepwm - d[n].bluepwm))
        x.reddiff = abs(x.redpwm - d[n].redpwm)
        x.greendiff = abs(x.greenpwm - d[n].greenpwm)
        x.bluediff = abs(x.bluepwm - d[n].bluepwm)
        u.append(maxdiff)
        n += 1
      maxdiff = max(u)
      for i in range(maxdiff/100):
        n = 1
        for x in t:
          if n > len(d): n = 1
          if 100*i <= x.reddiff:
            if x.redpwm < d[n].redpwm:
              pwm.set_pwm(x.redpin, 0, x.redpwm + 100*i)
            elif x.redpwm > d[n].redpwm:
              pwm.set_pwm(x.redpin, 0, x.redpwm - 100*i)
          else:
            pwm.set_pwm(x.redpin, 0, d[n].redpwm)
          if 100*i <= x.greendiff:
            if x.greenpwm < d[n].greenpwm:
              pwm.set_pwm(x.greenpin, 0, x.greenpwm + 100*i)
            elif x.greenpwm > d[n].greenpwm:
              pwm.set_pwm(x.greenpin, 0, x.greenpwm - 100*i)
          else:
            pwm.set_pwm(x.greenpin, 0, d[n].greenpwm)
          if 100*i <= x.bluediff:
            if x.bluepwm < d[n].bluepwm:
              pwm.set_pwm(x.bluepin, 0, x.bluepwm + 100*i)
            elif x.bluepwm > d[n].bluepwm:
              pwm.set_pwm(x.bluepin, 0, x.bluepwm - 100*i)
          else:
            pwm.set_pwm(x.bluepin, 0, d[n].bluepwm)
          n += 1
      n = 1
      for x in t:
        if n > len(d): n = 1
        x.redpwm = d[n].redpwm
        x.greenpwm = d[n].greenpwm
        x.bluepwm = d[n].bluepwm
        n += 1
      boo = not(boo)
      time.sleep(1)

  def randcolor(self):
    x = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return x

  def randomize(self):
      u = []
      d = {1:self.randcolor(),2:self.randcolor(),3:self.randcolor()}
      n = 1
      for x in t:
        if n > len(d): n = 1
        maxdiff = max(abs(x.redpwm - d[n].redpwm), abs(x.greenpwm - d[n].greenpwm), abs(x.bluepwm - d[n].bluepwm))
        x.reddiff = abs(x.redpwm - d[n].redpwm)
        x.greendiff = abs(x.greenpwm - d[n].greenpwm)
        x.bluediff = abs(x.bluepwm - d[n].bluepwm)
        u.append(maxdiff)
        n += 1
      maxdiff = max(u)
      for i in range(maxdiff/100):
        n = 1
        for x in t:
          if n > len(d): n = 1
          if 100*i <= x.reddiff:
            if x.redpwm < d[n].redpwm:
              pwm.set_pwm(x.redpin, 0, x.redpwm + 100*i)
            elif x.redpwm > d[n].redpwm:
              pwm.set_pwm(x.redpin, 0, x.redpwm - 100*i)
          else:
            pwm.set_pwm(x.redpin, 0, d[n].redpwm)
          if 100*i <= x.greendiff:
            if x.greenpwm < d[n].greenpwm:
              pwm.set_pwm(x.greenpin, 0, x.greenpwm + 100*i)
            elif x.greenpwm > d[n].greenpwm:
              pwm.set_pwm(x.greenpin, 0, x.greenpwm - 100*i)
          else:
            pwm.set_pwm(x.greenpin, 0, d[n].greenpwm)
          if 100*i <= x.bluediff:
            if x.bluepwm < d[n].bluepwm:
              pwm.set_pwm(x.bluepin, 0, x.bluepwm + 100*i)
            elif x.bluepwm > d[n].bluepwm:
              pwm.set_pwm(x.bluepin, 0, x.bluepwm - 100*i)
          else:
            pwm.set_pwm(x.bluepin, 0, d[n].bluepwm)
          n += 1
      n = 1
      for x in t:
        if n > len(d): n = 1
        x.redpwm = d[n].redpwm
        x.greenpwm = d[n].greenpwm
        x.bluepwm = d[n].bluepwm
        n += 1

  def randomsync(self):
    d = {1:red,2:green,3:blue,4:turquoise,5:purple,6:orange,7:white}
    for r in range(20):
      y = random.randint(1,7)
      for x in t:
        x.shift(d[y])
      time.sleep(5)

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

  def run(self):
    d = {'1':self.shift,'2':self.shift,'3':self.shift,'4':self.shift,
         '5':self.shift,'6':self.shift,'7':self.siren,'8':self.cyclecolors,
         'Ok':self.fadeoff,'0':self.shift}
    d2 = {'1':red,'2':green,'3':blue,'4':orange,'5':turquoise,'6':purple,
          '0':white}
    q = Queue.Queue()
    t1 = threading.Thread(target=self.checkcodes,args=(q,))
    t1.daemon = True
    t1.start()
    while True:
      try:
        y = q.get()
        if len(y) > 0:
          if y in d:
            try:
              t2.do_run = False
              t2.join()
            except: pass
            if y in d2:
              t2 = threading.Thread(target=d[y],args=(d2[y],))
              t2.daemon = True
              t2.start()
            else:
              t2 = threading.Thread(target=d[y])
              t2.daemon = True
              t2.start()
        time.sleep(.1)
      except KeyboardInterrupt:
        break
    try:
      t1.do_run = False
      t1.join()
      t2.do_run = False
      t2.join()
    except: pass

if __name__=="__main__":
  sys = System()
  try:
    sys.run()
  except KeyboardInterrupt:
    sys.turnoff()
    print "\nOH SHIT"
  print "Done"
