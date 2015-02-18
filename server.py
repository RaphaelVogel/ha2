import sys
import logging
from logging.handlers import RotatingFileHandler
from bottle import route, run, static_file

@route('/')
def home():
	return static_file('index.html', root='./web')

@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./web/static')

logger = logging.getLogger("HALogger")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler('ha.log', maxBytes=100000, backupCount=3)

logging.basicConfig(filename='./ha.log', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)
	
if len(sys.argv) > 1 and sys.argv[1] == 'devmode':
	run(host='localhost', port=8080, debug=True, reloader=True)
else:
	run(server='cherrypy' ,host='localhost', port=8080, debug=False, reloader=False)

