#-*-coding:utf-8-*-

import threading, multiprocessing, time, random
import socket
import json

class Executor(object):

  def __init__(self, props=None):
    self._port=3367
    self._host="127.0.0.1"
    if props :
      if props['host'] :
        self._host=props['host']
      if props['port'] :
        self._port=props['port']

  def listen(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((self._host,self._port))
    sock.listen(5)
  
    while True:
      print ("JobExecutor is listening - [%s:%d]"%(self._host, self._port ))
      connection, address = sock.accept()
      res = self.receive_request_body(connection)
      connection.close()
      print ("JobExecutor received jobs: %s"%(res))

  def receive_request_body(p_conn):
    result=[]
    rec_size=0
    while True:
      data = p_conn.recv(1024)
      if len(data) <= 0:
        break
      result.append(data)
      rec_size += len(data)
    return "".join(result)