#python modules
import os

#tornado modules
import tornado.ioloop
import tornado.web
import tornado.httpserver

#alarm server modules
from alarmserver.config import config
import logger

ALARMCLIENT = None

class ApiHandler(tornado.web.RequestHandler):
    def get(self):
        global ALARMCLIENT
        self.write(ALARMCLIENT._alarmstate)

class ApiConfigHandler(tornado.web.RequestHandler):
    def get(self, specific):
        self.write("doot")

def start(port, alarmclient, ssl_options = None):
    global ALARMCLIENT
    ALARMCLIENT = alarmclient
    logger.info("HTTP Server started on port: %s" % port) 
    ext_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ext')
    return tornado.httpserver.HTTPServer(tornado.web.Application([
        (r'/api/config/(.*)', ApiConfigHandler),
        (r'/api', ApiHandler),
        (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': ext_path}),
        (r'/(.*)', tornado.web.StaticFileHandler, {'default_filename' : 'index.html', 'path': ext_path}),
    ]),ssl_options=ssl_options).listen(port)

