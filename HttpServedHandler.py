import logging
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading

class RingBuffer():
    def __init__(self, size = 10):
        self.ls = [None for x in range(size)]
        
    def append(self, item):
        self.ls.pop(0)
        self.ls.append(item)
 
    def __getitem__(self, number):
        return self.ls[number]
    
    def __iter__(self):
        for x in self.ls:
            yield x
            
class LogHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>HTTPLogHandlerOutput</title></head><body bgcolor="black">')
        for record in self.server.log_messages:
            if record == None:
                break
            level, msg = record
            if level == 'ERROR':
                colour = 'red'
            elif level == 'WARNING':
                colour = 'yellow'
            else:
                colour = 'white'
            self.wfile.write('<font color="%s"><p>%s</p></font>' % (colour, msg))
        self.wfile.write('</body></html>')
        return
    
class LoggerHttpServer(HTTPServer):
    def __init__(self, server_address, log_messages):
        self.log_messages = log_messages
        HTTPServer.__init__(self, server_address, LogHandler)
        
class HttpServedHandler(logging.Handler):
    def __init__(self, port, daemon = True):
        logging.Handler.__init__(self) 
        self.data = RingBuffer(100)
        self.server = LoggerHttpServer(('', port), self.data)
        t = threading.Thread(target=self.server.serve_forever)
        t.daemon = daemon
        t.start()
    
    def emit(self, record):
        print record.levelname
        msg = self.format(record)
        self.data.append((record.levelname, msg))
        
