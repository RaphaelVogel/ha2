import tools.globals as glob
import sqlite3
import logging
from access_modules import weather

logger = logging.getLogger("ha_logger")


def start_job():
    current = weather.read_data(glob.fake)
    if not current:
        logger.error('Weather Job: Could not read weather values from sensors')
        return

    logger.debug('Weather Job: Temperature value: %s' % current['temperature'])
    logger.debug('Weather Job: Humidity value: %s' % current['humidity'])
    logger.debug('Weather Job: Pressure value: %s' % current['pressure'])
    try:
        con = sqlite3.connect('ha.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # check if temperature change is bigger than 8 C since the last chron run -> this is an outlier
        sqlstring = "select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 1"
        cur.execute(sqlstring)
        last = cur.fetchone()
        if not last['val_real']:
            # empty DB - first time
            cur.execute("insert into sensordata (device_id, sensor_id, val_real) VALUES (1,1,?)", (current['temperature'],))
        else:
            logger.debug('Last temperature value read from DB: %s' % last['val_real'])
            if current['temperature'] and abs(last['val_real'] - current['temperature']) <= 8:
                logger.debug('Insert new temperature value: %s' % current['temperature'])
                cur.execute('insert into sensordata (device_id, sensor_id, val_real) VALUES (1,1,?)', (current['temperature'],))
            else:
                logger.warn('Current temperature value %s is to different from last DB value %s: ' +
                            '-> Nothing inserted' % (current['temperature'], last['val_real']))
        con.commit()

        # check if humidity change is bigger than 10 %RH since the last chron run -> this is an outlier
        sqlstring = "select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 2"
        cur.execute(sqlstring)
        last = cur.fetchone()
        if not last['val_real']:
            # empty DB - first time
            cur.execute("insert into sensordata (device_id, sensor_id, val_real) VALUES (1,2,?)", (current['humidity'],))
        else:
            logger.debug('Last humidity value read from DB: %s' % last['val_real'])
            if current['humidity'] and abs(last['val_real'] - current['humidity']) <= 10:
                logger.debug('Insert new humidity value: %s' % current['humidity'])
                cur.execute('insert into sensordata (device_id, sensor_id, val_real) VALUES (1,2,?)', (current['humidity'],))
            else:
                logger.warn('Current humidity value %s is to different from last DB value %s: ' +
                            '-> Nothing inserted' % (current['humidity'], last['val_real']))
        con.commit()

        # check if pressure change is bigger than 3 mbar since the last chron run -> this is an outlier
        sqlstring = "select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 3"
        cur.execute(sqlstring)
        last = cur.fetchone()
        if not last['val_real']:
            # empty DB - first time
            cur.execute("insert into sensordata (device_id, sensor_id, val_real) VALUES (1,3,?)", (current['pressure'],))
        else:
            logger.debug('Last pressure value read from DB: %s' % last['val_real'])
            if current['pressure'] and abs(last['val_real'] - current['pressure']) <= 3:
                logger.debug('Insert new pressure value: %s' % current['pressure'])
                cur.execute('insert into sensordata (device_id, sensor_id, val_real) VALUES (1,3,?)', (current['pressure'],))
            else:
                logger.warn('Current pressure value %s is to different from last DB value %s: ' +
                            '-> Nothing inserted' % (current['pressure'], last['val_real']))
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
