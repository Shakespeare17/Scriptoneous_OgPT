import pyudev
import subprocess
import code

# Create a context for monitoring USB devices
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

# Start monitoring USB device events
for device in iter(monitor.poll, None):
    if device.action == 'add':
        # Open an interactive shell when a USB device is plugged in
        subprocess.call('clear', shell=True)  # Clear the terminal screen (optional)
        print(f"USB device plugged in: {device}")
        print("Opening interactive shell...\n")

        # Start an interactive shell for interacting with the device
        namespace = {'device': device}  # Pass the device object to the shell's namespace
        code.interact(local=namespace)

        print("Shell closed.\n")