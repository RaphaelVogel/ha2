import requests
import logging
from collections import OrderedDict

logger = logging.getLogger("ha_logger")

solar_data = OrderedDict()
solar_data['current'] = '5.49'
solar_data['current_unit'] = 'kW'
solar_data['day'] = '7.05'
solar_data['day_unit'] = 'kWh'
solar_data['month'] = '34.54'
solar_data['month_unit'] = 'kWh'
solar_data['year'] = '10.27'
solar_data['year_unit'] = 'MWh'
solar_data['total'] = '41.65'
solar_data['total_unit'] = 'MWh'

def read_data(fake=None):
    ''' Reads data from the solar inverter and returns it as Dictionary. In case of an error None is returned'''
    if fake:
        return solar_data
    try:
        resp = requests.get('http://192.168.1.19/data/ajax.txt?CAN=1&HASH=00100401&TYPE=5', 
            headers={'Accept':'*/*'}, auth=('customer', '********'), timeout=3)
    except Exception as e:
        logger.error('Could not read data from solar inverter: %s' % str(e))
        return
    
    logger.debug('Response from solar inverter %s' % resp.content)
    # example body
    # master;5.47 kW;5.47 kVA;0.00 kvar;7.05 kWh;7.05 kVAh;0.00 kvarh;34.54 kWh;34.54 kVAh;0.00 kvarh;10.10 MWh;10.10 MVAh;0.00 Mvarh;31.10 MWh;31.10 MVAh;0.00 Mvarh;
    # 1;AT 5000;2.91 kW;4.1 kWh;16.44 MWh;0055A1701029;268435492;3;00100401;0
    # 2;NT 4200;2.53 kW;3.4 kWh;14.66 MWh;0044A0313104;268435492;3;00200402;0
    split_content = resp.text.split(';')
    if split_content[0] != 'master':
        logger.warn('Incorect data format from solar inverter')
        return

    current_data = split_content[1].split()
    solar_data['current'] = current_data[0]
    solar_data['current_unit'] = current_data[1]
    day_data = split_content[4].split();
    solar_data['day'] = day_data[0];
    solar_data['day_unit'] = day_data[1];
    month_data = split_content[7].split()
    solar_data['month'] = month_data[0]
    solar_data['month_unit'] = month_data[1]
    year_data = split_content[10].split()
    solar_data['year'] = year_data[0]
    solar_data['year_unit'] = year_data[1]
    total_data = split_content[13].split()
    solar_data['total'] = total_data[0]
    solar_data['total_unit'] = total_data[1]
    
    logger.debug('Dictionary values created from solar inverter %s' % str(solar_data))
    return solar_data
