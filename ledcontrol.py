import Adafruit_PCA9685
import time, random

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(200)
	
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

  def blink(self, color):
    blinkspeed = .05
    for y in range(10):
      for x in t:
        x.turnon(color)
      time.sleep(blinkspeed)
      for x in t:
        x.turnoff()
      time.sleep(blinkspeed)

  def siren(self):
    for i in range(50):
      for x in t:
        x.turnon(red)
      time.sleep(.25)
      for x in t:
        x.turnoff()
        x.turnon(blue)
      time.sleep(.25)
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
    for i in range(maxdiff/10):
      for x in t:
        if 10*i <= x.reddiff:
          if x.redpwm < tocolor.redpwm:
            pwm.set_pwm(x.redpin, 0, x.redpwm + 10*i)
          elif x.redpwm > tocolor.redpwm:
            pwm.set_pwm(x.redpin, 0, x.redpwm - 10*i)
        else:
          pwm.set_pwm(x.redpin, 0, tocolor.redpwm)
        if 10*i <= x.greendiff:
          if x.greenpwm < tocolor.greenpwm:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm + 10*i)
          elif x.greenpwm > tocolor.greenpwm:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm - 10*i)
        else:
          pwm.set_pwm(x.greenpin, 0, tocolor.greenpwm)
        if 10*i <= x.bluediff:
          if x.bluepwm < tocolor.bluepwm:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm + 10*i)
          elif x.bluepwm > tocolor.bluepwm:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm - 10*i)
        else:
          pwm.set_pwm(x.bluepin, 0, tocolor.bluepwm)
    for x in t:
      pwm.set_pwm(x.redpin, 0, tocolor.redpwm)
      pwm.set_pwm(x.greenpin, 0, tocolor.greenpwm)
      pwm.set_pwm(x.bluepin, 0, tocolor.bluepwm)
      x.redpwm = tocolor.redpwm
      x.greenpwm = tocolor.greenpwm
      x.bluepwm = tocolor.bluepwm

  def cyclecolors(self, cyctime):
    for x in t:
      x.turnon(red)
    time.sleep(cyctime)
    for x in t:
      x.turnon(orange)
    time.sleep(cyctime)
    for x in t:
      x.turnon(yellow)
    time.sleep(cyctime)
    for x in t:
      x.turnon(green)
    time.sleep(cyctime)
    for x in t:
      x.turnon(blue)
    time.sleep(cyctime)
    for x in t:
      x.turnon(turquoise)
    time.sleep(cyctime)
    for x in t:
      x.turnon(purple)
    time.sleep(cyctime)
    for x in t:
      x.turnon(white)
    time.sleep(cyctime)
    for x in t:
      x.turnoff()

  def christmas(self):
    d = {1:red, 2:green, 3:white}
    u = []
    n = 1
    for x in t:
      maxdiff = max(abs(x.redpwm - d[n].redpwm), abs(x.greenpwm - d[n].greenpwm), abs(x.bluepwm - d[n].bluepwm))
      x.reddiff = abs(x.redpwm - d[n].redpwm)
      x.greendiff = abs(x.greenpwm - d[n].greenpwm)
      x.bluediff = abs(x.bluepwm - d[n].bluepwm)
      u.append(maxdiff)
      n += 1
    maxdiff = max(u)
    for i in range(maxdiff/10):
      n = 1
      for x in t:
        if 10*i <= x.reddiff:
          if x.redpwm < d[n].redpwm:
            pwm.set_pwm(x.redpin, 0, x.redpwm + 10*i)
          elif x.redpwm > d[n].redpwm:
            pwm.set_pwm(x.redpin, 0, x.redpwm - 10*i)
        else:
          pwm.set_pwm(x.redpin, 0, d[n].redpwm)
        if 10*i <= x.greendiff:
          if x.greenpwm < d[n].greenpwm:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm + 10*i)
          elif x.greenpwm > d[n].greenpwm:
            pwm.set_pwm(x.greenpin, 0, x.greenpwm - 10*i)
        else:
          pwm.set_pwm(x.greenpin, 0, d[n].greenpwm)
        if 10*i <= x.bluediff:
          if x.bluepwm < d[n].bluepwm:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm + 10*i)
          elif x.bluepwm > d[n].bluepwm:
            pwm.set_pwm(x.bluepin, 0, x.bluepwm - 10*i)
        else:
          pwm.set_pwm(x.bluepin, 0, d[n].bluepwm)
        n += 1
      
if __name__=="__main__":
  sys = System()
  led1 = LED(0,1,2)
  led2 = LED(3,4,5)
  led3 = LED(6,7,8)
  try:
    sys.christmas()
    time.sleep(1)
    sys.fadeoff()
  except KeyboardInterrupt:
    sys.turnoff()
    print "\nOH SHIT"
print "Done"

