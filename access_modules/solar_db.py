import sqlite3
import logging

logger = logging.getLogger("ha_logger")


def read_data(year=None, month=None):
    retdata = {"solar_data": []}
    sqlstring = None
    if not year:
        # return average production per year
        sqlstring = ("select strftime('%Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 2 and sensor_id = 1 group by strftime('%Y',timestamp)")
        logger.debug('Executed SQL statement to read average solardata per year: %s' % sqlstring)

    if year and not month:
        # return average production per month for specified year
        sqlstring = ("select strftime('%m %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 2 and sensor_id = 1 and strftime('%Y',timestamp) = '" + year + "' group by strftime('%m %Y',timestamp)")
        logger.debug('Executed SQL statement to read average solardata per month for year %s: %s' % (year, sqlstring))

    if year and month:
        # return per day production for specified month
        sqlstring = (
            "select strftime('%d.%m. %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
            "where device_id = 2 and sensor_id = 1 and strftime('%Y',timestamp) = '" + year + "' and strftime('%m',timestamp) = '" + month + "' group by strftime('%d.%m. %Y',timestamp)")
        logger.debug('Executed SQL statement to read average solardata per day for month %s in year %s: %s' % (
            month, year, sqlstring))

    try:
        con = sqlite3.connect('./ha2/ha.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sqlstring)
        all_rows = cur.fetchall()
        for row in all_rows:
            retdata['solar_data'].append({'time': row['time'], 'value': row['value']})

        return retdata

    except Exception as e:
        logger.error('Could not read solar data from DB: %s' % str(e))
        return

    finally:
        con.close()
