import sqlite3
import logging
from logging.handlers import RotatingFileHandler
from access_modules import solar
from datetime import datetime

# logger configuration
logger = logging.getLogger("ha_logger")
logger.setLevel(logging.DEBUG)
filehandler = RotatingFileHandler('./log.txt', maxBytes=100000, backupCount=3)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)


def start_job():
    """This function is called several times from cron, because I do not know when the solar inverter
    switches off. It always updates the day production
    """
    current = solar.read_data()
    if not current:
        logger.debug('Solar Job: Could not read solar values from sensors')
        return

    logger.debug('Solar Job: day production value: %s' % current['day'])
    try:
        con = sqlite3.connect('ha.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        now = datetime.now()
        today_string = str(datetime.date(now))
        # check if there is already an entry for today
        cur.execute("select val_real from sensordata where device_id = 2 and sensor_id = 1 and strftime('%Y-%m-%d',timestamp) = ?", (today_string,))
        last = cur.fetchone()
        if not last:
            # first value for today
            logger.debug('Insert first day production value to DB %s' % current['day'])
            cur.execute("insert into sensordata (device_id, sensor_id, val_real) VALUES (2,1,?)", (current['day'],))
        else:
            # we have an entry and solar converter is still running, so update the value
            logger.debug('Update day production with value %s' % current['day'])
            sqlstring = "update sensordata set val_real = ? where device_id = 2 and sensor_id = 1 and strftime('%Y-%m-%d',timestamp) = ?"
            cur.execute(sqlstring, (current['day'], today_string))

        con.commit()

    except Exception as e:
        logger.error('Could not run solar_job: %s' % str(e))
        return

    finally:
        con.close()

    return

if __name__ == '__main__':
    logger.debug('Starting solar job')
    start_job()
    logger.debug('Solar job stopped')

