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
                jsonobj = json.loads(data.decode())
                sendno=jsonobj["sendno"]
                msg=jsonobj["message"]
                print (msg, 'from', address)

                #stream.write(msg.decode().strip())
                #yield stream.write( msg[::-1] )
                stream.write(("I got["+str(sendno)+"]...\n").encode())
                if msg == 'over':
                    stream.close()
        except iostream.StreamClosedError:
            pass
        
if __name__ == '__main__':
    server = MyTcpServer()
    server.listen( 8036 )
    server.start()
    print ("Server starts ...")
    ioloop.IOLoop.current().start()
    print ("Server starts listen on 8036...")
