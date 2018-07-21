# -*- coding: utf-8 -*-

import random, traceback, time
from multiprocessing import Process
 
class Mate(Process):

  def __init__(self):
    Process.__init__(self)
    
  def run(self):
    try:
      while True:
        print ("process[%s] is running..."%(self.pid))  
        time.sleep(2)
    except:
      traceback.print_exc()
      
if __name__ == '__main__':
  pids = []
  for i in range(5):
    mate = Mate()
    pids.append(mate)
    mate.start()
    
  time.sleep(10)
  randompid = random.randint(0, 4)
  print ("start to terminate process[%d]"%( randompid ))
  pids[randompid].terminate()
  time.sleep(2)
  print ("process[%d] is alive: %s"%( randompid, pids[randompid].is_alive() ))