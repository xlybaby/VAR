# -*- coding: utf-8 -*-

import json
import time

from tornado import ioloop, gen, iostream
from tornado.tcpclient import TCPClient

class TestTcpclient(object):
    """docstring for TestTcpClient"""
    def __init__(self, host,port):
        self.host = host
        self.port = port
        self.sendno = 10000
 
    @gen.coroutine
    def start(self):
      self.stream = yield TCPClient().connect(self.host, self.port)
  
      try:

        while True:
          self.sendno =self.sendno + 1
          message={"sendno":self.sendno,"message":"register node"}
          encode_json = json.dumps(message)  
          print ("send "+str(self.sendno))
          self.stream.write(encode_json.encode()+b"\n")
          rec=yield self.stream.read_until(b'\n')
          print ('recive from the server',rec)
          time.sleep(2)
      except iostream.StreamClosedError:
        pass
 
def test_main():
    tcp_client = TestTcpclient('localhost', 8036)
    tcp_client.start()
    ioloop.IOLoop.current().start()
    
test_main()