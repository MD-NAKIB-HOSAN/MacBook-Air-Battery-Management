import psutil
import time
import subprocess

# Global variables to store previous battery status
previous_status = None

def send_notification(message):
    """Send a macOS notification."""
    script = f'display notification "{message}" with title "Battery Monitor"'
    subprocess.run(["osascript", "-e", script])

def get_battery_status():
    # Get battery information
    battery = psutil.sensors_battery()
    if battery is None:
        print("Unable to fetch battery status.")
        return None
    
    percent = battery.percent
    plugged = battery.power_plugged
    
    # Determine the battery status message
    if percent == 19 and not plugged:
        message = "Warning!!!! Battery level getting low. Consider charging."
    elif percent > 79 and plugged:
        message = "Alert!!! Battery above 79%. Consider unplugging."
    else:
        message = "Hoorraayyyy!!!...Battery is within the desired range. Keep using."
    
    return message, percent

def main():
    global previous_status
    
    while True:
        status_message, percent = get_battery_status()
        
        if status_message is None:
            time.sleep(60)  # Retry after 60 seconds if battery status cannot be retrieved
            continue

        # Only send a notification if the status has changed
        if previous_status is None or previous_status != status_message:
            send_notification(status_message)
            previous_status = status_message  # Update previous status

        time.sleep(60)  # Delay of 60 seconds before checking again

if __name__ == "__main__":
    main()
