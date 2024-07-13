import sys

from plyer import notification
from sensorServer import SensorServer


def __main__():
    print('Room name: ', end='')
    room_name = input()
    print('Server IP: ', end='')
    ip_addr = input()
    sensor = None
    try:
        sensor = SensorServer(ip_addr)
    except (TimeoutError, ConnectionRefusedError):
        print('Could not connect to the sensor')
        sys.exit(1)
    except OSError as e:
        print(f'Invalid IP address ({e})')
        sys.exit(1)
    print('Connected')
    sensor_enabled = True
    while sensor_enabled:
        message = sensor.await_message()
        match message:
            case SensorServer.MOTION_DETECTED:
                notification.notify(title='Door Monitor', message=f'Activity detected {room_name}!', timeout=10)
            case SensorServer.DISCONNECT:
                notification.notify(title='Door Monitor', message=f'Sensor for {room_name} has been disabled', timeout=10)
                sys.exit(0)
            case None:
                notification.notify(title='Door Monitor', message=f'Sensor for {room_name} has failed', timeout=10)
                sys.exit(1)

if __name__ == '__main__':
    __main__()