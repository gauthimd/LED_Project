import Adafruit_PCA9685
import time
x = 409
red = 2
green = 1
blue = 0
blinkspeed = .1
blinkrange = 20
sirenrange = 20
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(100)
def turnon(color):
  pwm.set_pwm(color, 0, 4095)
def turnoff(color):
  pwm.set_pwm(color, 0, 0)
def fadeon(color):
  for i in range(0, x):
    pwm.set_pwm(color, 0, 10*i)
    time.sleep(.001)
def fadeoff(color):
  for i in range(0, x):
    pwm.set_pwm(color, 0, 4095-10*i)
    time.sleep(.001)
  pwm.set_pwm(color, 0, 0)
def fadeonoff(color):
  for i in range(0, x):
    pwm.set_pwm(color, 0, 10*i)
    time.sleep(.001)
  for i in range(0, x):
    pwm.set_pwm(color, 0, 4095-10*i)
    time.sleep(.001)
  pwm.set_pwm(color, 0, 0)
def blink(color):
  for i in range(blinkrange):
    pwm.set_pwm(color, 0, 4000)
    time.sleep(blinkspeed)
    pwm.set_pwm(color, 0, 0)
    time.sleep(blinkspeed)
def siren():
  for i in range(sirenrange):
    turnon(red)
    time.sleep(.1)
    turnoff(red)
    turnon(blue)
    time.sleep(.1)
    turnoff(blue)
def shift(fromcolor, tocolor):
  for i in range(0, x):
    pwm.set_pwm(fromcolor, 0, 4095-10*i)
    pwm.set_pwm(tocolor, 0, 10*i)
    time.sleep(.001)
  pwm.set_pwm(fromcolor, 0, 0)
turnon(red)
time.sleep(2)
turnoff(red)
time.sleep(.5)
fadeon(green)
time.sleep(2)
fadeoff(green)
time.sleep(.5)
fadeonoff(blue)
blink(red)
blink(green)
blink(blue)
siren()
time.sleep(.5)
fadeon(red)
shift(red, green)
time.sleep(2)
shift(green,blue)
time.sleep(2)
shift(blue, red)
time.sleep(2)
fadeoff(red)
print "Done"
