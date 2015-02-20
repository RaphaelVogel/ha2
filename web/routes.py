import tools.globals as globals
from bottle import route, static_file, request, HTTPResponse
from access_modules import solar, solar_db, weather, weather_db

@route('/')
def index():
    return static_file('index.html', root='./web')

@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./web/static')


# Solar inverter API
# -------------------------------------------------------------------
@route('/solar/current')
def current_solarproduction():
    current_data = solar.read_data(globals.fake) # returns a dictionary, will be transformed to JSON by bottle
    if current_data:
        return current_data
    else:
        return HTTPResponse(dict(error="Could not read solar production values"), code=500)

@route('/solar/historicProduction')
def historic_production():
    year = request.query.year
    month = request.query.month
    historic_data = solar_db.read_data(year, month)
    if historic_data:
        return historic_data
    else:
        return HTTPResponse(dict(error="Could not read solar production values from DB"), code=500)


# Weather data API
# -------------------------------------------------------------------
@route('/weather/current')
def current_weather():
    current_data = weather.read_data(globals.fake)
    if current_data:
        return current_data
    else:
        return HTTPResponse(dict(error="Could not read weather data values"), code=500)

@route('/weather/historicTemperatures')
def historic_temperatures():
    year = request.query.year
    month = request.query.month
    day = request.query.day
    historic_data = weather_db.read_temperature(year, month, day)
    if historic_data:
        return historic_data
    else:
        return HTTPResponse(dict(error="Could not read temperature values form DB"), code=500)

@route('/weather/historicHumidities')
def historic_humidities():
    year = request.query.year
    month = request.query.month
    day = request.query.day
    historic_data = weather_db.read_humidity(year, month, day)
    if historic_data:
        return historic_data
    else:
        return HTTPResponse(dict(error="Could not read humiditiy values form DB"), code=500)

@route('/weather/historicPressures')
def historic_pressures():
    year = request.query.year
    month = request.query.month
    day = request.query.day
    historic_data = weather_db.read_pressure(year, month, day)
    if historic_data:
        return historic_data
    else:
        return HTTPResponse(dict(error="Could not read pressure values form DB"), code=500)