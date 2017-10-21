import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(100)


class Color(object):
    def __init__(self, red, green, blue):
        self.red_pwm = int(red * 16.059)  # Convert 8 bits to 12 bits
        self.green_pwm = int(green * 16.059)
        self.blue_pwm = int(blue * 16.059)


red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
orange = Color(255, 255, 0)
turquoise = Color(0, 255, 255)
purple = Color(255, 0, 255)
grey = Color(55, 55, 55)


class LED(object):
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

    def turn_on(self, color):
        pwm.set_pwm(self.red_pin, 0, color.red_pwm)
        pwm.set_pwm(self.green_pin, 0, color.green_pwm)
        pwm.set_pwm(self.blue_pin, 0, color.blue_pwm)

    def turn_off(self):
        pwm.set_pwm(self.red_pin, 0, 0)
        pwm.set_pwm(self.green_pin, 0, 0)
        pwm.set_pwm(self.blue_pin, 0, 0)

    def fade_on(self, color):
        limit = max(color.red_pwm, color.green_pwm, color.blue_pwm)
        # while 10 * i <= limit:
        for i in xrange(limit):
            if 10 * i >= limit:
                break
            if 10 * i <= color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, 10 * i)
            else:
                pwm.set_pwm(self.red_pin, 0, color.red_pwm)
            if 10 * i <= color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, 10 * i)
            else:
                pwm.set_pwm(self.green_pin, 0, color.green_pwm)
            time.sleep(.001)
            if 10 * i <= color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, 10 * i)
            else:
                pwm.set_pwm(self.blue_pin, 0, color.blue_pwm)
            time.sleep(.001)

    def fade_off(self, color):
        limit = max(color.red_pwm, color.green_pwm, color.blue_pwm)
        # while 10 * i <= limit:
        for i in xrange(limit):
            '''
            if you can (which you usually can) you should avoid 'while' loops...
                'for' loops always have a stopping point; 'while' loops can do the Energizer bunny thing,
                which can crash your machine
            
            another thought here is to limit the loop to the xrange of the limit/10,
            and then you can remove the break clause entirely, 
            but I would want to test this to verify
            that it's what you want.... ie, that the math actually works. 
            
            so it would look like:
            for i in xrange(limit/10):
                if 10 * i <= color.red_pwm:
                    pwm.set_pwm(self.red_pin, 0, color.red_pwm - 10 * i)
            etc.
            '''
            if 10 * i >= limit:
                break
            if 10 * i <= color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, color.red_pwm - 10 * i)
            else:
                pwm.set_pwm(self.red_pin, 0, 0)
            if 10 * i <= color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, color.green_pwm - 10 * i)
            else:
                pwm.set_pwm(self.green_pin, 0, 0)
            time.sleep(.001)
            if 10 * i <= color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, color.blue_pwm - 10 * i)
            else:
                pwm.set_pwm(self.blue_pin, 0, 0)
            time.sleep(.001)
        pwm.set_pwm(self.red_pin, 0, 0)
        pwm.set_pwm(self.green_pin, 0, 0)
        pwm.set_pwm(self.blue_pin, 0, 0)

    def fade_on_off(self, color):
        limit = max(color.red_pwm, color.green_pwm, color.blue_pwm)
        for i in xrange(limit):
            if 10 * i >= limit:
                break
            if 10 * i <= color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, 10 * i)
            else:
                pwm.set_pwm(self.red_pin, 0, color.red_pwm)
            if 10 * i <= color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, 10 * i)
            else:
                pwm.set_pwm(self.green_pin, 0, color.green_pwm)
            if 10 * i <= color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, 10 * i)
            else:
                pwm.set_pwm(self.blue_pin, 0, color.blue_pwm)

        for i in xrange(limit):
            if 10 * i >= limit:
                break
            if 10 * i <= color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, color.red_pwm - 10 * i)
            else:
                pwm.set_pwm(self.red_pin, 0, 0)
            if 10 * i <= color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, color.green_pwm - 10 * i)
            else:
                pwm.set_pwm(self.green_pin, 0, 0)
            if 10 * i <= color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, color.blue_pwm - 10 * i)
            else:
                pwm.set_pwm(self.blue_pin, 0, 0)
            i += 1
        pwm.set_pwm(self.red_pin, 0, 0)
        pwm.set_pwm(self.green_pin, 0, 0)
        pwm.set_pwm(self.blue_pin, 0, 0)

    def blink(self, color):
        blink_speed = .05
        for x in range(10):
            self.turn_on(color)
            time.sleep(blink_speed)
            self.turn_off()
            time.sleep(blink_speed)

    def siren(self):
        for i in xrange(10):
            self.turn_on(red)
            time.sleep(.1)
            self.turn_off()
            self.turn_on(blue)
            time.sleep(.1)
            self.turn_off()

    def shift(self, from_color, to_color):
        max_diff = max(abs(from_color.red_pwm - to_color.red_pwm), abs(from_color.green_pwm - to_color.green_pwm),
                       abs(from_color.blue_pwm - to_color.blue_pwm))
        i = 0
        while 10 * i <= max_diff:
            if from_color.red_pwm < to_color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, from_color.red_pwm + 10 * i)
            elif from_color.red_pwm > to_color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, from_color.red_pwm - 10 * i)
            if from_color.green_pwm < to_color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, from_color.green_pwm + 10 * i)
            elif from_color.green_pwm > to_color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, from_color.green_pwm - 10 * i)
            if from_color.blue_pwm < to_color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, from_color.blue_pwm + 10 * i)
            elif from_color.blue_pwm > to_color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, from_color.blue_pwm - 10 * i)
            i += 1
        pwm.set_pwm(self.red_pin, 0, to_color.red_pwm)
        pwm.set_pwm(self.green_pin, 0, to_color.green_pwm)
        pwm.set_pwm(self.blue_pin, 0, to_color.blue_pwm)

    def slow_shift(self, from_color, to_color):
        max_diff = max(abs(from_color.red_pwm - to_color.red_pwm), abs(from_color.green_pwm - to_color.green_pwm),
                       abs(from_color.blue_pwm - to_color.blue_pwm))
        for i in xrange(max_diff):
            if from_color.red_pwm < to_color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, from_color.red_pwm + i)
            elif from_color.red_pwm > to_color.red_pwm:
                pwm.set_pwm(self.red_pin, 0, from_color.red_pwm - i)
            if from_color.green_pwm < to_color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, from_color.green_pwm + i)
            elif from_color.green_pwm > to_color.green_pwm:
                pwm.set_pwm(self.green_pin, 0, from_color.green_pwm - i)
            if from_color.blue_pwm < to_color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, from_color.blue_pwm + i)
            elif from_color.blue_pwm > to_color.blue_pwm:
                pwm.set_pwm(self.blue_pin, 0, from_color.blue_pwm - i)
        pwm.set_pwm(self.red_pin, 0, to_color.red_pwm)
        pwm.set_pwm(self.green_pin, 0, to_color.green_pwm)
        pwm.set_pwm(self.blue_pin, 0, to_color.blue_pwm)

    def test(self):
        self.turn_on(red)
        time.sleep(.5)
        self.turn_off()
        time.sleep(.33)
        self.fade_on(green)
        time.sleep(.5)
        self.fade_off(green)
        time.sleep(.33)
        self.fade_on_off(blue)
        time.sleep(.33)
        self.siren()
        time.sleep(.33)
        self.blink(orange)
        time.sleep(.33)
        self.fade_on(turquoise)
        self.shift(turquoise, purple)
        self.shift(purple, green)
        self.slow_shift(green, purple)
        self.fade_off(purple)


if __name__ == "__main__":
    led1 = LED(2, 1, 0)
    led1.test()
    print "Yeah"
