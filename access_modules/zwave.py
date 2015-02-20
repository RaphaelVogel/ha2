import requests
import logging

logger = logging.getLogger("ha_logger")

def read_devices_status(fake=None):
    device_state = {'livingroom_light':'OFF'}
    if fake:
        return device_state

    # read status of livingroom light
    try:
        resp = requests.post('http://haserver:8083/ZWaveAPI/Run/devices[2].instances[0].SwitchBinary.data.level.value')
        logger.debug('Response from livingroom light status: %s' % resp.content)
        device_state['livingroom_light'] = 'OFF' if resp.content == 'false' else 'ON'
        return device_state
    except Exception as e:
        logger.error('Could not read the status of the livingroom light: %s' % str(e))
        return None


def set_livingroom_light(state, fake=None):
    '''Switches the light on or off. <state> must be 'ON' or 'OFF' '''
    device_state = {'livingroom_light':state}
    if fake:
        return device_state
    
    on_off = 255 if state == 'ON' else 0
    try:
        resp = requests.post('http://haserver:8083/ZWaveAPI/Run/devices[2].instances[0].SwitchBinary.Set('+on_off+')')
        
    except Exception as e:
        logger.error('Could not switch the livingroom light %s: %s' % (state, str(e)))
        return None
