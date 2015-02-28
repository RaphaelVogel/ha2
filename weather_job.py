#!/usr/bin/python3
import sqlite3, logging
from logging.handlers import RotatingFileHandler
from access_modules import weather

# logger configuration
logger = logging.getLogger("ha_logger")
logger.setLevel(logging.WARN)
filehandler = RotatingFileHandler('./ha2/log.txt', maxBytes=100000, backupCount=3)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)


def start_job():
    current = weather.read_data()
    if not current:
        logger.error('Weather Job: Could not read weather values from sensors')
        return

    logger.debug('Weather Job: Temperature value: %s' % current['temperature'])
    logger.debug('Weather Job: Humidity value: %s' % current['humidity'])
    logger.debug('Weather Job: Pressure value: %s' % current['pressure'])
    try:
        con = sqlite3.connect('./ha2/ha.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # check if temperature change is bigger than 10 C since the last chron run -> this is an outlier
        sqlstring = "select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 1"
        cur.execute(sqlstring)
        last = cur.fetchone()
        if not last['val_real']:
            # empty DB - first time
            cur.execute("insert into sensordata (device_id, sensor_id, val_real) VALUES (1,1,?)", (current['temperature'],))
        else:
            logger.debug('Last temperature value read from DB: %s' % last['val_real'])
            if current['temperature'] and abs(last['val_real'] - current['temperature']) <= 10:
                logger.debug('Insert new temperature value: %s' % current['temperature'])
                cur.execute('insert into sensordata (device_id, sensor_id, val_real) VALUES (1,1,?)', (current['temperature'],))
            else:
                logger.warn('Current temperature value %s is to different from last DB value %s: -> Nothing inserted' % (current['temperature'], last['val_real']))
        con.commit()

        # check if humidity change is bigger than 20 %RH since the last chron run -> this is an outlier
        sqlstring = "select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 2"
        cur.execute(sqlstring)
        last = cur.fetchone()
        if not last['val_real']:
            # empty DB - first time
            cur.execute("insert into sensordata (device_id, sensor_id, val_real) VALUES (1,2,?)", (current['humidity'],))
        else:
            logger.debug('Last humidity value read from DB: %s' % last['val_real'])
            if current['humidity'] and abs(last['val_real'] - current['humidity']) <= 20:
                logger.debug('Insert new humidity value: %s' % current['humidity'])
                cur.execute('insert into sensordata (device_id, sensor_id, val_real) VALUES (1,2,?)', (current['humidity'],))
            else:
                logger.warn('Current humidity value %s is to different from last DB value %s: -> Nothing inserted' % (current['humidity'], last['val_real']))
        con.commit()

        # check if pressure change is bigger than 4 mbar since the last chron run -> this is an outlier
        sqlstring = "select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 3"
        cur.execute(sqlstring)
        last = cur.fetchone()
        if not last['val_real']:
            # empty DB - first time
            cur.execute("insert into sensordata (device_id, sensor_id, val_real) VALUES (1,3,?)", (current['pressure'],))
        else:
            logger.debug('Last pressure value read from DB: %s' % last['val_real'])
            if current['pressure'] and abs(last['val_real'] - current['pressure']) <= 4:
                logger.debug('Insert new pressure value: %s' % current['pressure'])
                cur.execute('insert into sensordata (device_id, sensor_id, val_real) VALUES (1,3,?)', (current['pressure'],))
            else:
                logger.warn('Current pressure value %s is to different from last DB value %s: -> Nothing inserted' % (current['pressure'], last['val_real']))
        con.commit()

    except Exception as e:
        logger.error('Could not run weather_job: %s' % str(e))
        return

    finally:
        con.close()

    return

if __name__ == '__main__':
    logger.debug('Starting weather job')
    start_job()
    logger.debug('Weather job stopped')
