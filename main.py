import subprocess
import time

from gpiozero import OutputDevice


ON_THRESHOLD = 65  # (ºC) Fan starts spinning above this temp.
SLEEP_INTERVAL = 5  # (seconds) How often to check the temperature.
GPIO_PIN = 14  # Which GPIO pin you're using to control the fan (DEFAULT = 14).

def main():
    fan = OutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()

        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        if temp > ON_THRESHOLD and not fan.value:
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < ON_THRESHOLD:
            fan.off()

        time.sleep(SLEEP_INTERVAL)

def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True) # Run shell command to check temp.
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0]) # Extract temperature from output.
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')

if __name__ == '__main__':
    main()