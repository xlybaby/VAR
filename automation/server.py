# -*- coding: utf-8 -*-

import json

from tornado import ioloop, gen, iostream
from tornado.tcpserver import TCPServer

class MyTcpServer( TCPServer ):
    
    @gen.coroutine
    def handle_stream( self, stream, address ):
        try:
            while True:
                data = yield stream.read_until(b"\n")
                #msg = yield stream.read_bytes( 20, partial = True )
                #jsonobj = json.loads(data.decode())
                #sendno=jsonobj["sendno"]
                #msg=jsonobj["message"]
                print (data, 'from', address)

                #stream.write(msg.decode().strip())
                #yield stream.write( msg[::-1] )
                stream.write(("I got message...\n").encode())
                if data == 'over':
                    stream.close()
        except iostream.StreamClosedError:
            pass
        
if __name__ == '__main__':
    server = MyTcpServer()
    server.listen( 8087 )
    server.start()
    
    server = MyTcpServer()
    server.listen( 8088 )
    server.start()
    
    server = MyTcpServer()
    server.listen( 8089 )
    server.start()
    print ("Server starts ...")
    ioloop.IOLoop.current().start()
    print ("Server starts listen on 8088...")
