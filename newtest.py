#!/usr/bin/env python
import Queue, threading, time, lirc
sockid = lirc.init("myprog", blocking=False)

class System():
    
  def Run(self):
      d = {"1":self.mode1,"2":self.mode2}
      q = Queue.Queue()
      t1 = threading.Thread(target=self.checkcodes,args=(q,))
      t1.daemon = True  # so you can quit the demo program easily :)
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
              t2 = threading.Thread(target=d[y])
              t2.daemon = True
              t2.start()
            elif y == "Ok": break
            else: pass
          time.sleep(.1)
        except KeyboardInterrupt: 
          break
      try:
        t1.do_run = False
        t1.join()
        t2.do_run = False
        t2.join()
      except: pass
  
  def checkcodes(self, q):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
      try:
        x = lirc.nextcode()
        y = ""
        for n in x:
           y = x[0].encode('utf-8')
        q.put(y)
        time.sleep(.1)
      except KeyboardInterrupt: break
  
  def mode1(self):
    delay = 1
    initim = time.time()
    then = initim + delay
    t = threading.currentThread()
    while getattr(t, "do_run", True):
      now = time.time()
      if now < then: pass
      else:
        print "I'm doing stuff"
        then = now + delay
      time.sleep(.001)
    print "you killed me"
  
  def mode2(self):
    delay = 1
    initim = time.time()
    then = initim + delay
    t = threading.currentThread()
    while getattr(t, "do_run", True):
      now = time.time()
      if now < then: pass
      else:
        print "I'm doing stuff 2"
        then = now + delay
      time.sleep(.001)
    print "you killed me 2"

if __name__ == '__main__':
   sys = System()
   sys.Run()
