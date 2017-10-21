import Adafruit_PCA9685
import time, random

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(100)

class Color():

  def __init__(self, red, green, blue):
    self.redpwm = int(red*16.059)   #Convert 8 bits to 12 bits 
    self.greenpwm = int(green*16.059)   
    self.bluepwm = int(blue*16.059)

red = Color(255,0,0)
green = Color(0,255,0)
blue = Color(0,0,255)
orange = Color(255,255,0)
turquoise = Color(0,255,255)
purple = Color(255,0,255)
gray = Color(100,100,100)

class LED():

  def __init__(self, redpin, greenpin, bluepin):
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(100)
    self.redpin = redpin
    self.greenpin = greenpin
    self.bluepin = bluepin

  def turnon(self, color):
    pwm.set_pwm(self.redpin, 0, color.redpwm)
    pwm.set_pwm(self.greenpin, 0, color.greenpwm)
    pwm.set_pwm(self.bluepin, 0, color.bluepwm)

  def turnoff(self):
    pwm.set_pwm(self.redpin, 0, 0)
    pwm.set_pwm(self.greenpin, 0, 0)
    pwm.set_pwm(self.bluepin, 0, 0)

  def fadeon(self, color):
    limit = max(color.redpwm, color.greenpwm, color.bluepwm)
    for i in range(limit/10):
      if 10*i <= color.redpwm:
        pwm.set_pwm(self.redpin, 0, 10*i)
      else:
        pwm.set_pwm(self.redpin, 0, color.redpwm) 
      if 10*i <= color.greenpwm:
        pwm.set_pwm(self.greenpin, 0, 10*i)
      else:
        pwm.set_pwm(self.greenpin, 0, color.greenpwm) 
      time.sleep(.001)
      if 10*i <= color.bluepwm:
        pwm.set_pwm(self.bluepin, 0, 10*i)
      else:
        pwm.set_pwm(self.bluepin, 0, color.bluepwm) 
      time.sleep(.001)
    pwm.set_pwm(self.redpin, 0, color.redpwm)
    pwm.set_pwm(self.greenpin, 0, color.greenpwm)
    pwm.set_pwm(self.bluepin, 0, color.bluepwm)   

  def fadeoff(self, color):
    limit = max(color.redpwm, color.greenpwm, color.bluepwm)
    for i in range(limit/10):
      if 10*i <= color.redpwm:
        pwm.set_pwm(self.redpin, 0, color.redpwm - 10*i)
      else:
        pwm.set_pwm(self.redpin, 0, 0) 
      if 10*i <= color.greenpwm:
        pwm.set_pwm(self.greenpin, 0, color.greenpwm - 10*i)
      else:
        pwm.set_pwm(self.greenpin, 0, 0) 
      time.sleep(.001)
      if 10*i <= color.bluepwm:
        pwm.set_pwm(self.bluepin, 0, color.bluepwm - 10*i)
      else:
        pwm.set_pwm(self.bluepin, 0, 0) 
      time.sleep(.001)
    pwm.set_pwm(self.redpin, 0, 0)
    pwm.set_pwm(self.greenpin, 0, 0)
    pwm.set_pwm(self.bluepin, 0, 0)  

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
      time.sleep(.1)
      self.turnoff()
      self.turnon(blue)
      time.sleep(.1)
      self.turnoff()

  def shift(self, fromcolor, tocolor):
    maxdiff = max(abs(fromcolor.redpwm - tocolor.redpwm), abs(fromcolor.greenpwm - tocolor.greenpwm), abs(fromcolor.bluepwm - tocolor.bluepwm))
    reddiff = abs(fromcolor.redpwm - tocolor.redpwm)
    greendiff = abs(fromcolor.greenpwm - tocolor.greenpwm)
    bluediff = abs(fromcolor.bluepwm - tocolor.bluepwm)
    for i in range(maxdiff/10):
      if 10*i <= reddiff:
        if fromcolor.redpwm < tocolor.redpwm:
          pwm.set_pwm(self.redpin, 0, fromcolor.redpwm + 10*i)
        elif fromcolor.redpwm > tocolor.redpwm:
          pwm.set_pwm(self.redpin, 0, fromcolor.redpwm - 10*i)
      else:
        pwm.set_pwm(self.redpin, 0, tocolor.redpwm)
      if 10*i <= greendiff:
        if fromcolor.greenpwm < tocolor.greenpwm:
          pwm.set_pwm(self.greenpin, 0, fromcolor.greenpwm + 10*i)
        elif fromcolor.greenpwm > tocolor.greenpwm:
          pwm.set_pwm(self.greenpin, 0, fromcolor.greenpwm - 10*i)
      else:
        pwm.set_pwm(self.greenpin, 0, tocolor.greenpwm)
      if 10*i <= bluediff:
        if fromcolor.bluepwm < tocolor.bluepwm:
          pwm.set_pwm(self.bluepin, 0, fromcolor.bluepwm + 10*i)
        elif fromcolor.bluepwm > tocolor.bluepwm:
          pwm.set_pwm(self.bluepin, 0, fromcolor.bluepwm - 10*i)
      else:
        pwm.set_pwm(self.bluepin, 0, tocolor.bluepwm)
    pwm.set_pwm(self.redpin, 0, tocolor.redpwm)
    pwm.set_pwm(self.greenpin, 0, tocolor.greenpwm)
    pwm.set_pwm(self.bluepin, 0, tocolor.bluepwm)

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
    x = Color(random.randint(0,255),random.randint(0,255),0)
    return x

  def randomshifter(self):
    i = self.randcolor()
    j = self.randcolor()
    self.fadeon(i)
    time.sleep(2)
    for x in range(5):
      self.shift(i,j)
      time.sleep(2)
      i = j
      j = self.randcolor()
    self.fadeoff(i)

  def test(self):
    self.turnon(red)
    time.sleep(1)
    self.turnoff()
    self.fadeon(green)
    time.sleep(1)
    self.fadeoff(green)
    time.sleep(1)
    self.siren()
    time.sleep(1)
    self.fadeon(turquoise)
    time.sleep(1)
    self.shift(turquoise, gray)
    time.sleep(1)
    self.fadeoff(gray)
    time.sleep(1)
    self.blink(orange)
    
if __name__=="__main__":
  led1 = LED(2,1,0)
  led1.test()
  print "Yeah"

