import sys
import logging

from plyer import notification
from sensorServer import SensorServer


def __main__():
    logging.basicConfig()
    room_name = input('Room name: ')
    ip_addr = input('Server Address: ')
    log_file = input('Log File (leave blank to disable logging): ')
       # configure the logger
    log_active = True
    if log_file.strip() == '':
        print('Logging disabled')
        log_active = False
    else:
        logging.basicConfig(filename=log_file, filemode='a+', format='%(asctime)s: %(message)s')
    # configure the sensor
    sensor = None
    try:
        sensor = SensorServer(ip_addr)
    except (TimeoutError, ConnectionRefusedError):
        print('Could not connect to the sensor')
        sys.exit(1)
    except OSError as e:
        print(f'Invalid IP address ({e})')
        sys.exit(1)
    # await a message from the door monitor
    print('Connected')
    sensor_enabled = True
    while sensor_enabled:
        message = sensor.await_message()
        match message:
            case SensorServer.MOTION_DETECTED:
                notification.notify(title='Door Monitor', message=f'Activity detected in {room_name}!', timeout=10)
                if log_active:
                    logging.info(f'{room_name}: Activity Detected')
            case SensorServer.DISCONNECT:
                notification.notify(title='Door Monitor', message=f'Sensor for {room_name} has been disabled', timeout=10)
                if log_active:
                    logging.info(f'{room_name}: Sensor Disconnected')
                sys.exit(0)
            case None:
                notification.notify(title='Door Monitor', message=f'Sensor for {room_name} has failed', timeout=10)
                if log_active:
                    logging.info(f'{room_name}: Sensor Failure')
                sys.exit(1)

if __name__ == '__main__':
    __main__()
