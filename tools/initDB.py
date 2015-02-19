import sqlite3

con = sqlite3.connect('../ha.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS device (device_id INTEGER NOT NULL, name TEXT NOT NULL, type TEXT, location TEXT, picture BLOB, PRIMARY KEY(device_id))")
cur.execute("CREATE TABLE IF NOT EXISTS sensor (device_id INTEGER NOT NULL, sensor_id INTEGER NOT NULL, name TEXT, type TEXT, unit TEXT, PRIMARY KEY(device_id, sensor_id))")
cur.execute("CREATE TABLE IF NOT EXISTS sensordata (device_id INTEGER NOT NULL, sensor_id INTEGER NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, val_string TEXT, val_int INTEGER, val_real REAL)")

# Weather station
cur.execute("INSERT OR IGNORE INTO device (device_id, name, type) VALUES (1, 'Wetter Station', 'Tinkerforge')")
cur.execute("INSERT OR IGNORE INTO sensor (device_id, sensor_id, name, type, unit) VALUES (1, 1, 'Temperatur Sensor', 'Tinkerforge', 'Grad')")
cur.execute("INSERT OR IGNORE INTO sensor (device_id, sensor_id, name, type, unit) VALUES (1, 2, 'Luftfeuchtigkeit', 'Tinkerforge', '%RH')")
cur.execute("INSERT OR IGNORE INTO sensor (device_id, sensor_id, name, type, unit) VALUES (1, 3, 'Luftdruck', 'Tinkerforge', 'mBar')")

# Solar inverter
cur.execute("INSERT OR IGNORE INTO device (device_id, name, type) VALUES (2, 'Solar Inverter', 'Sunways')")
cur.execute("INSERT OR IGNORE INTO sensor (device_id, sensor_id, name, type, unit) VALUES (2, 1, 'Solar Inverter', 'Sunways', 'kWH')")

con.commit()
con.close()