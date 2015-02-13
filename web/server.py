import sys
from bottle import route, run, static_file

@route('/')
def home():
	return static_file('index.html', root='./')

@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')
	
if len(sys.argv) > 1 and sys.argv[1] == 'devmode':
	run(host='localhost', port=8080, debug=True, reloader=True)
else:
	run(server='cherrypy' ,host='localhost', port=8080, debug=False, reloader=False)