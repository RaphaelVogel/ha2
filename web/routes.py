import tools.globals as globals
from bottle import route, static_file
import access_modules.solar as solar

@route('/')
def index():
    return static_file('index.html', root='./web')

@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./web//static')

@route('/solar/current')
def read_current_solarproduction():
    current_data = solar.read_data(globals.fake)
    # bottle automatically converts dictionaries to JSON
    return current_data 