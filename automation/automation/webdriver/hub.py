# -*- coding: utf-8 -*-

import time
import threading
import errno
import functools
import socket
import asyncio
import json
import socket

import tornado.ioloop
from tornado import gen
from tornado.iostream import IOStream
from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError

from automation.common.application import Configure

class StreamHandler( object ):
    
    @staticmethod
    def startlisten(p_name, p_prefix, p_queue, p_delimiter):
      port = Configure.configure().value(p_key=p_prefix+".port")
      host = Configure.configure().value(p_key=p_prefix+".host")
      sendBufferSize = Configure.configure().value(p_key=p_prefix+".sendBufferSize")
      recvBufferSize = Configure.configure().value(p_key=p_prefix+".recvBufferSize")
      
      server=StreamHandler( p_name=p_name, p_host=host, p_port=port, p_sendBufferSize=sendBufferSize, p_recvBufferSize=recvBufferSize, p_queue=p_queue, p_delimiter=p_delimiter )
      #server.listen( port )
      print ("Server["+p_name+"] starts at "+str(port)+"...")
      server.start()

    def __init__(self, p_name, p_host, p_port, p_sendBufferSize, p_recvBufferSize, p_queue, p_max_buffer_size=None, p_read_chunk_size=None, p_delimiter="\n"):
      TCPServer.__init__(self, max_buffer_size=p_max_buffer_size, read_chunk_size=p_read_chunk_size)
      self._name = p_name
      self._host = p_host
      self._port = p_port
      
      self._send_buffer_size = p_sendBufferSize
      self._recv_buffer_size = p_recvBufferSize
      
      self._delimiter = p_delimiter
      self._queue = p_queue
      
      self._request_waiting_timeout = Configure.configure().value(p_key="headless.webdriver.requestWaittingTimeout")
    
    def getName(self):
      return self._name
                 
    #@gen.coroutine
    def start( self ):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      # set send buffer size
      sock.setsockopt( socket.SOL_SOCKET, socket.SO_SNDBUF, self._send_buffer_size)
      # set recieve buffer size
      sock.setsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF, self._recv_buffer_size)
      #sock.setblocking(0)
      sock.bind((self._host, self._port))
      sock.listen(128)
      while True:
        conn, addr = sock.accept()
        print ("Get connection accept")
        request = {"conn":conn, "addr":addr, "delimiter":self._delimiter}
        self._queue.put(request, block=True, timeout=Configure.configure().value("headless.webdriver.requestWaittingTimeout"))
        print ("Put connection to queue")