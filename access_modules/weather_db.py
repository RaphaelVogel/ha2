import sqlite3, logging

logger = logging.getLogger("ha_logger")


def read_temperature(year=None, month=None, day=None):
    retdata = {"temp_data": []}
    sqlstring = None
    if not year:
        # return average temp per year
        sqlstring = ("select strftime('%Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 1 and sensor_id = 1 group by strftime('%Y',timestamp)")
        logger.debug('Executed SQL statement to read average temperature per year: %s' % sqlstring)

    if year and not month and not day:
        # return average temp per month for specified year
        sqlstring = ("select strftime('%m %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 1 and sensor_id = 1 and strftime('%Y',timestamp) = '" + year + "' group by strftime('%m %Y',timestamp)")
        logger.debug('Executed SQL statement to read average temperature per month for year %s: %s' % (year, sqlstring))

    if year and month and not day:
        # return average temp per day for specified month
        sqlstring = (
            "select strftime('%d.%m. %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
            "where device_id = 1 and sensor_id = 1 and strftime('%Y',timestamp) = '" + year + "' and strftime('%m',timestamp) = '" + month + "' group by strftime('%d.%m. %Y',timestamp)")
        logger.debug('Executed SQL statement to read average temperature per day for month %s in year %s: %s' % (
            month, year, sqlstring))

    if year and month and day:
        # return temp values for a single day
        sqlstring = ("select strftime('%H:%M',timestamp) as time, val_real as value from sensordata " +
                     "where device_id = 1 and sensor_id = 1 and strftime('%Y',timestamp) = '" + year + "' and strftime('%m',timestamp) = '" + month + "' and strftime('%d',timestamp) = '" + day + "'")
        logger.debug(
            'Executed SQL statement to read temperature values for %s.%s.%s: %s' % (day, month, year, sqlstring))

    try:
        con = sqlite3.connect('./ha2/ha.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sqlstring)
        all_rows = cur.fetchall()
        for row in all_rows:
            retdata['temp_data'].append({'time': row['time'], 'value': row['value']})

        minval, maxval = get_min_max(retdata['temp_data'])
        retdata['min'] = minval
        retdata['max'] = maxval
        return retdata

    except Exception as e:
        logger.error('Could not read temperature data from DB: %s' % str(e))
        return

    finally:
        con.close()


def read_humidity(year=None, month=None, day=None):
    retdata = {"humidity_data": []}
    sqlstring = None
    if not year:
        # return average humidity per year
        sqlstring = ("select strftime('%Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 1 and sensor_id = 2 group by strftime('%Y',timestamp)")
        logger.debug('Executed SQL statement to read average humidity per year: %s' % sqlstring)

    if year and not month and not day:
        # return average humidity per month for specified year
        sqlstring = ("select strftime('%m %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 1 and sensor_id = 2 and strftime('%Y',timestamp) = '" + year + "' group by strftime('%m %Y',timestamp)")
        logger.debug('Executed SQL statement to read average humidity per month for year %s: %s' % (year, sqlstring))

    if year and month and not day:
        # return average humidity per day for specified month
        sqlstring = (
            "select strftime('%d.%m. %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
            "where device_id = 1 and sensor_id = 2 and strftime('%Y',timestamp) = '" + year + "' and strftime('%m',timestamp) = '" + month + "' group by strftime('%d.%m. %Y',timestamp)")
        logger.debug('Executed SQL statement to read average humidity per day for month %s in year %s: %s' % (
            month, year, sqlstring))

    if year and month and day:
        # return humidity values for a single day
        sqlstring = ("select strftime('%H:%M',timestamp) as time, val_real as value from sensordata " +
                     "where device_id = 1 and sensor_id = 2 and strftime('%Y',timestamp) = '" + year + "' and strftime('%m',timestamp) = '" + month + "' and strftime('%d',timestamp) = '" + day + "'")
        logger.debug('Executed SQL statement to read humidity values for %s.%s.%s: %s' % (day, month, year, sqlstring))

    try:
        con = sqlite3.connect('./ha2/ha.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sqlstring)
        all_rows = cur.fetchall()
        for row in all_rows:
            retdata['humidity_data'].append({'time': row['time'], 'value': row['value']})

        minval, maxval = get_min_max(retdata['humidity_data'])
        retdata['min'] = minval
        retdata['max'] = maxval
        return retdata

    except Exception as e:
        logger.error('Could not read humidity data from DB: %s' % str(e))
        return

    finally:
        con.close()


def read_pressure(year=None, month=None, day=None):
    retdata = {"pressure_data": []}
    sqlstring = None
    if not year:
        # return average pressure per year
        sqlstring = ("select strftime('%Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 1 and sensor_id = 3 group by strftime('%Y',timestamp)")
        logger.debug('Executed SQL statement to read average pressure per year: %s' % sqlstring)

    if year and not month and not day:
        # return average pressure per month for specified year
        sqlstring = ("select strftime('%m %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
                     "where device_id = 1 and sensor_id = 3 and strftime('%Y',timestamp) = '" + year + "' group by strftime('%m %Y',timestamp)")
        logger.debug('Executed SQL statement to read average pressure per month for year %s: %s' % (year, sqlstring))

    if year and month and not day:
        # return average pressure per day for specified month
        sqlstring = (
            "select strftime('%d.%m. %Y',timestamp) as time, round(avg(val_real),2) as value from sensordata " +
            "where device_id = 1 and sensor_id = 3 and strftime('%Y',timestamp) = '" + year + "' and strftime('%m',timestamp) = '" + month + "' group by strftime('%d.%m. %Y',timestamp)")
        logger.debug('Executed SQL statement to read average pressure per day for month %s in year %s: %s' % (
            month, year, sqlstring))

    if year and month and day:
        # return pressure values for a single day
        sqlstring = ("select strftime('%H:%M',timestamp) as time, val_real as value from sensordata " +
                     "where device_id = 1 and sensor_id = 3 and strftime('%Y',timestamp) = '" + year + "' and strftime('%m',timestamp) = '" + month + "' and strftime('%d',timestamp) = '" + day + "'")
        logger.debug('Executed SQL statement to read pressure values for %s.%s.%s: %s' % (day, month, year, sqlstring))

    try:
        con = sqlite3.connect('./ha2/ha.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sqlstring)
        all_rows = cur.fetchall()
        for row in all_rows:
            retdata['pressure_data'].append({'time': row['time'], 'value': row['value']})

        minval, maxval = get_min_max(retdata['pressure_data'])
        retdata['min'] = minval
        retdata['max'] = maxval
        return retdata

    except Exception as e:
        logger.error('Could not read pressure data from DB: %s' % str(e))
        return

    finally:
        con.close()


def get_min_max(list_of_dicts):
    minval = 1200
    maxval = -30
    for current_dict in list_of_dicts:
        if current_dict['value'] > maxval:
            maxval = current_dict['value']
        if current_dict['value'] < minval:
            minval = current_dict['value']

    minval = round(minval) - 3
    maxval = round(maxval) + 3
    return minval, maxval
