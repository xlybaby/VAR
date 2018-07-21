# -*- coding: utf-8 -*-

import asyncio, datetime, json, queue, uuid, time, threading, traceback
from multiprocessing import Process,Manager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import tornado.ioloop

from automation.common.logging import Logger
from automation.common.network import ServerWrapper
from automation.common.application import Configure

def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                  ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class DriverProcess(threading.Thread):

  def __init__(self, p_request_queue, p_alive_timeout=None):
    threading.Thread.__init__(self)
    self._iniWinHeight = Configure.configure().value("headless.webdriver.iniBrowserWinHeight")
    self._iniWinWidth = Configure.configure().value("headless.webdriver.iniBrowserWinWidth")
    self._driver_path = Configure.configure().value("headless.webdriver.path")

    self._input = queue.Queue(1)
    self._output = asyncio.Queue(maxsize=1)
    
    self._alive_timeout = p_alive_timeout
    
    self._request_queue = p_request_queue
    self._events = {
      "getPage": self.getPage,
      "snapshot": self.getSnapShot
    }

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size="+str(self._iniWinWidth)+"x"+str(self._iniWinHeight))
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self._driver_path)
    self._driverwrapper = {"driver": driver, "instancetime": datetime.datetime.now(), "lastactivetime": datetime.datetime.now(), "usetimes": 0 }
  
  def getDriverwrapper(self):
    return self._driverwrapper

  def getInputQueue(self):
    return self._input 

  def getOutputQueue(self):
    return self._output 

  def getPage(self, p_body):
    #driverwrapper = None
    try:
      flag = p_body["flag"] if "flag" in p_body else None
      addr = p_body["addr"] if "addr" in p_body else None
      if addr == None:
        return "None"
      Logger.getLogger().info("Get page source: %s"%(addr))
       
      #driverwrapper = self._driver_queue.get(timeout=Configure.configure().value("headless.webdriver.freeDriverWaittingTimeout")) 
      #Logger.getLogger().info("Got driver")
      self._driverwrapper["lastactivetime"] = datetime.datetime.now()
      self._driverwrapper["usetimes"] = self._driverwrapper["usetimes"] + 1
        
      driver = self._driverwrapper["driver"]
      driver.set_page_load_timeout(Configure.configure().value("headless.webdriver.driverGetPageTimeout"))
      #await asyncio.sleep(40)
      driver.get( addr )  
      Logger.getLogger().info("Get page source done")
      return driver.page_source 
    except queue.Empty:
      Logger.getLogger().error("Driver pool is empty")
      #return json.dumps({"status": StatusCode.ERROR, "message": "No available driver"})    
      return "None"
    except TimeoutException:
      Logger.getLogger().error("Driver get page timeout")
      #return json.dumps({"status": StatusCode.ERROR, "message": "No available driver"})    
      return "None"
    finally:
      pass
#       try:
#         if driverwrapper != None:
#           self._driver_queue.put(driverwrapper, block=False)
#           Logger.getLogger().info("Return driver") 
#       except:
#         pass
        
  def getSnapShot(self, p_body):
    #driverwrapper = None
    try:
      addr = p_body["addr"] if "addr" in p_body else None
      if addr == None:
        return "None"
    
      #driverwrapper = self._driver_queue.get(timeout=Configure.configure().value("headless.webdriver.freeDriverWaittingTimeout")) 
      self._driverwrapper["lastactivetime"] = datetime.datetime.now()
      self._driverwrapper["usetimes"] = self._driverwrapper["usetimes"] + 1
       
      driver = self._driverwrapper["driver"]
      
      driver.get(addr)
      clientHeight = driver.execute_script("return document.body.clientHeight;")
      cursize = driver.get_window_size()
      driver.set_window_size(cursize["width"], clientHeight)
    
      base64 = driver.get_screenshot_as_base64( addr )  
      driver.set_window_size(cursize["width"], cursize["height"])
      
      return base64 
    except queue.Empty:
      Logger.getLogger().error("Driver pool is empty")  
      #return json.dumps({"status": StatusCode.ERROR, "message": "No available driver"})    
      return "None"
    finally:
      pass
#       try:
#         if driverwrapper != None:
#           self._driver_queue.put(driverwrapper, block=False) 
#       except:
#         pass
  
  async def execute(self, input):
      print ("##### driver got request", input) 
      if input == "Over":
        driver = self._driverwrapper["driver"]  
        driver.quit()  
        return
      try:
        body = json.loads(input)  
        event = body["event"] if "event" in body else None
        if event == None:
          self._output.put_nowait("None")
          return  
          #return json.dumps({"status": StatusCode.ERROR, "message": "Unknown event type"})    
        res = await self._events[event](body) 
        print ("##### driver got response", res) 
        self._output.put_nowait(res) 
      except:
        traceback.print_exc() 
               
  def run(self):
    try:
      while True:
        
        print ("##### driver waiting for request")  
        request = self._request_queue.get(block=True, timeout=self._alive_timeout)#self._input.get()
        print ("##### driver got request", request) 
        
        try:
          conn = request["conn"]
          delimiter = request["delimiter"]
          subnum = 0 - len(delimiter)
          #data = stream.read_until(delimiter.encode())
          data = b''
          bary = bytearray(1024)
          bread = 0
          while True:
            print ("##### driver recv message")  
            bread = conn.recv_into(bary)
            if bread == 0:
              break;
            print ("##### driver got %d bytes"%(bread), bary[0:bread])
            data = data + bary[0:bread]
            print ("##### data array: ", data, data[subnum:], delimiter.encode())
            if len(data)>len(delimiter) and data[subnum:]==delimiter.encode():
              break
          print ("##### driver got all message", data)
          #message = "".join(data)
          #message = message[:subnum]
          
          body = json.loads(data[:subnum])  
          event = body["event"] if "event" in body else None
          print ("##### driver got request event", event)
          if event == None:
            stream.write(b"None"+delimiter.encode())
            continue  
            #return json.dumps({"status": StatusCode.ERROR, "message": "Unknown event type"})    
          res = self._events[event](body) 
          print ("##### driver got response", res)
          #stream.write(res.encode()+delimiter.encode())
          conn.sendall(res.encode()+delimiter.encode())
          
        except:
          traceback.print_exc()  
          
    except queue.Empty:
      print ("This driver process is end of life, quit!")
      driver = self._driverwrapper["driver"]
      if driver:
        driver.quit()
      #traceback.print_exc()
      
    '''A thread class that supports raising exception in the thread from
       another thread.
    '''
  def _get_my_tid(self):
    """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
    """
    if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

    # do we have it cached?
    if hasattr(self, "_thread_id"):
            return self._thread_id

    # no, look for it in the _active dict
    for tid, tobj in threading._active.items():
      if tobj is self:
        self._thread_id = tid
        return tid

    # TODO: in python 2.6, there's a simpler way to do : self.ident
    raise AssertionError("could not determine the thread's id")

  def raiseExc(self, exctype):
    """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
    """
    _async_raise( self._get_my_tid(), exctype )