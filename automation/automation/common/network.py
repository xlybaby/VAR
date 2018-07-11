# -*- coding: utf-8 -*-

import time
import threading
import errno
import functools
import socket
import asyncio
import json

import tornado.ioloop
from tornado import gen
from tornado.iostream import IOStream
from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError

from automation.common.application import Configure

class ServerWrapper(object):

  def __init__(self):
    pass

  @staticmethod
  def listen(p_name, p_prefix, p_handler):
    port = Configure.configure().value(p_key=p_prefix+".port")
#     sbuf = Configure.configure().value(p_key=p_prefix+".sendBufferSize")
#     rbuf = Configure.configure().value(p_key=p_prefix+".recvBufferSize")
#     delimiter = Configure.configure().value(p_key=p_prefix+".delimiter")
#     s=Server(p_port=port, p_callback=p_handler, p_delimiter=delimiter, p_recv_buf=rbuf)
#     s.listen()
    server=SimpleTcpServer( p_name=p_name, p_callback=p_handler )
    server.listen( port )
    server.start()
    print ("Server["+p_name+"] starts at "+str(port)+"...")
    #tornado.ioloop.IOLoop.current().start()
    #print ("Server starts listen on " + str(port))

class SimpleTcpServer( TCPServer ):
    
    def __init__(self, p_name, p_callback, p_max_buffer_size=None, p_read_chunk_size=None):
      TCPServer.__init__(self, max_buffer_size=p_max_buffer_size, read_chunk_size=p_read_chunk_size)
      self._callback = p_callback
      self._name = p_name
#     def startListen(self):
#       self.listen( self._port )
#       self.start()
#       ioloop.IOLoop.current().start()
    
    def getName(self):
      return self._name
                 
    @gen.coroutine
    def handle_stream( self, stream, address ):
        try:
            while True:
                #print ("server starts waiting...")
                data = yield stream.read_until(b"\n")
                #jsonobj = json.loads(data.decode())
                #sendno=jsonobj["sendno"]
                #msg=jsonobj["message"]
                #msg = yield stream.read_bytes( 20, partial = True )
                print (data, 'from', address)
                ret = self._callback.callback(p_message=data)
                #encode_ret = json.dumps(ret)
                stream.write(ret.encode()+b"\n")
                #stream.write(msg.decode().strip())
                #yield stream.write( msg[::-1] )
                #if data == 'over':
                    #stream.close()
        except StreamClosedError:
            pass
            
class Server(object):
  
  def __init__(self, p_port, p_callback, p_delimiter, p_send_buf=4096, p_recv_buf=4096):
    #super(Server, self).__init__()
    self._callback = p_callback
    self._port = p_port
    self._send_buf_size = p_send_buf
    self._recv_buf_size = p_recv_buf
    self._delimiter = p_delimiter
    
  @gen.coroutine
  def handle_connection(self, connection, address):
    stream = IOStream(connection)
    print ("start handle request...")
    #message = yield stream.read_until_close()
    message = yield stream.read_bytes( 20, partial = True )
    #print ("delimiter: ", chr(self._delimiter).encode())
    #stream.read_until(chr(self._delimiter).encode(), self.on_body)
    print("message from client:", message.decode().strip())
    
  def on_body(self, data):
    print("message from client:", data.decode().strip())
    self._callback.callback(p_message=data.decode().strip())
    
  def connection_ready(self, sock, fd, events):
    while True:
      #try:
      print ("waiting for request...")
      connection, address = sock.accept()
      print ("request coming...")
      #except socket.error as e:
      #  if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
      #    raise
      #  return
      connection.setblocking(0)
      self.handle_connection(connection, address)

  def start(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # set send buffer size
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_SNDBUF, self._send_buf_size)
    # set recieve buffer size
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF, self._recv_buf_size)
    sock.setblocking(0)
    sock.bind(("", self._port))
    sock.listen(128)
    print ("Initial socket done.")
    io_loop = tornado.ioloop.IOLoop.current()
    callback = functools.partial(self.connection_ready, sock)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    print ("ioloop start...")
    io_loop.start()
    print ("ioloop started...")
     
class ClientWrapper(object):

  def __init__(self):
    self._clients={}
    
  def addClient(self, p_server_map, p_name):
    client = Client(p_server_map=p_server_map)
    self._clients[p_name]=client
  
  def getClient(self, p_name): 
    return self._clients[p_name]

class SimpleTcpclient(object):

    def __init__(self, p_mq, p_server_map, p_callback=None, max_buffer_size=None, timeout=None):
      self._host = p_server_map["host"]
      self._port = p_server_map["port"]
      self._max_buf_size = max_buffer_size
      self._timeout = timeout
      self._mq = p_mq
      self._handler = p_callback
      self._tcpclient = TCPClient()
    
    def setHandler(self, p_callback): 
      self._handler = p_callback
           
    @gen.coroutine
    def start(self):
      try:
        print ("Connecting remote server", self._host, self._port)
        self._stream = yield self._tcpclient.connect(self._host, self._port, max_buffer_size=self._max_buf_size, timeout=self._timeout)
        print ("Remote server connected", self._host, self._port)
      except StreamClosedError:
        self._stream = None
        print ("Tcp client starts error, remote server connection couldn't reach.", self._host, self._port, self._max_buf_size, self._timeout)
      
      while True:
        try:     
          print("waiting message from queue...")
          data = self._mq.get(block=True) 
          if self._stream == None :
            print ("Tcp client start to send message, but the stream is closed")
            try:
              self._stream = yield self._tcpclient.connect(self._host, self._port, max_buffer_size=self._max_buf_size, timeout=self._timeout)
            except StreamClosedError:
              self._stream = None
              print ("Tcp client re-starts error, remote server connection couldn't reach.", self._host, self._port, self._max_buf_size, self._timeout)
              print ("message abandoned => ", data)
              continue
          
          sendmsg = json.dumps(data)
          self._stream.write(sendmsg.encode()+b"\n")
          #rec=yield self._stream.read_until(b'\n')
          #fut=self._stream.read_until(b'\n')
          #print (fut)
          rec = yield from asyncio.wait_for(self._stream.read_until(b'\n'), 10)
          print ("rec",rec)
          if self._handler:
            self._handler(data=rec)
        except StreamClosedError:
          self._stream = None  
          print ("remote server's connection is closed.")
        except asyncio.TimeoutError:  
          print ("Reading from server occurs timeout exception.")
          self._stream = None
              
    def close(self):
      if self._stream:
        self._stream.close()
        self._stream = None
             
class Client(threading.Thread):
  
  def send_request(self):
    index=0  
    while True:  
      #try:
        print("waiting message from queue...")
        msg = self._mq.get(block=True)
        print ("send message: ", str(index)+msg)  
        
        self._stream.write((str(index)+msg).encode(), self.on_body)
        index=index+1
        #self._stream.read_until(b"\n", self.on_body)
       #self._stream.read_until(b"\r\n\r\n", self.on_headers)
      #except e:
      #  print (e);

  
  def on_headers(self, data):
    headers = {}
    for line in data.split(b"\r\n"):
       parts = line.split(b":")
       if len(parts) == 2:
           headers[parts[0].strip()] = parts[1].strip()
    self._stream.read_bytes(int(headers[b"Content-Length"]), on_body)

  def on_body(self, data):
    print ("message from server: ", data)  
#     self._stream.close()
#     tornado.ioloop.IOLoop.current().stop()
  
  def __call__(self):
    self.send_request()
           
  def __init__(self, p_mq, p_server_map):
    super(Client, self).__init__()
    self._target_host = p_server_map["host"]
    self._target_port = p_server_map["port"]
    self._mq = p_mq
  
  #def run(self): 
    #asyncio.set_event_loop(asyncio.new_event_loop())  
    #thread = threading.current_thread()
    #print ("current thread: ",thread.getName())  
    #print ("current thread io_loop: ",io_loop)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.setblocking(0)
    #callback = functools.partial(self.send_request, sock)
    self._stream = tornado.iostream.IOStream(sock)
    #print ("connect server...")
    self._stream.connect((self._target_host, self._target_port), self.send_request)
    print ("client ioloop start...")
    tornado.ioloop.IOLoop.current().start()
    print ("client ioloop started")