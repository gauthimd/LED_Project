import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(200)

class LED():

  def __init__(self, redpin, greenpin, bluepin):
    self.redpin = redpin
    self.greenpin = greenpin
    self.bluepin = bluepin
    self.redpwm = 0
    self.greenpwm = 0
    self.bluepwm = 0
    self.bright = 1

  def turnon(self, color):
    pwm.set_pwm(self.redpin, 0, int(color.redpwm*self.bright))
    pwm.set_pwm(self.greenpin, 0, int(color.greenpwm*self.bright))
    pwm.set_pwm(self.bluepin, 0, int(color.bluepwm*self.bright))
    self.redpwm = int(color.redpwm*self.bright)
    self.greenpwm = int(color.greenpwm*self.bright)
    self.bluepwm = int(color.bluepwm*self.bright)

  def turnoff(self):
    pwm.set_pwm(self.redpin, 0, 0)
    pwm.set_pwm(self.greenpin, 0, 0)
    pwm.set_pwm(self.bluepin, 0, 0)
    self.redpwm = 0
    self.greenpwm = 0
    self.bluepwm = 0

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

