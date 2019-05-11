#!/usr/bin/python3
'''
Enable tap-to-click only after a period of touchpad activity.
My goal is to prevent stray clicks.

Uses /dev/input/eventN to watch for touchpad activity and
gsettings to enable and disable tap-to-click.

I had to add myself the the 'input' group to get access
to the device.

Gary Bishop May 2019
'''

import evdev
from select import select
from subprocess import run
import argparse

parser = argparse.ArgumentParser(description='Manage tap-to-click on the touchpad')
parser.add_argument('-v', action='store_true', help='show tap-to-click state')
parser.add_argument('--device', help='path to touchpad device')
parser.add_argument('--tap_delay', type=float, default=0.5,
                    help='time to wait before enabling tap-to-click')
parser.add_argument('--max_wait_idle', type=float, default=0.25,
                    help='max idle time while waiting to enable tap')
parser.add_argument('--max_tap_idle', type=float, default=1.0,
                    help='max idle time before disabling tap again')
args = parser.parse_args()

verbose = args.v

def tapToClick(on):
    '''Control tap-to-click'''
    if verbose:
        print('tap', on)
    run(['/usr/bin/gsettings',
         'set',
         'org.gnome.desktop.peripherals.touchpad',
         'tap-to-click',
         'true' if on else 'false'
         ], check=True)


# find the touchpad
if not args.device:
    for path in evdev.list_devices():
        tp = evdev.InputDevice(path)
        if 'touchpad' in tp.name.lower():
            break
    else:
        raise RuntimeError('Touchpad not found')
else:
    tp = evdev.InputDevice(args.device)

# define the states
idle, wait, tap = 'idle wait tap'.split()

# Configure the various times
tap_delay = args.tap_delay  # time active before enabling tap to click
# timeouts for the select while waiting for events
timeout = {
    idle: None,
    wait: args.max_wait_idle,
    tap: args.max_tap_idle,
}

# start in the idle state with tap off
tapToClick(False)
state = idle
try:
    while True:
        # wait for an event or timeout
        r, w, x, = select([tp.fd], [], [], timeout[state])
        if not r:  # timeout
            if state == tap:
                tapToClick(False)
            state = idle
            continue

        # get the event
        event = tp.read_one()
        # if idle enter the wait state and remember the time
        if state == idle:
            state = wait
            t0 = event.timestamp()

        # if in wait and its been long enough, enable tap
        elif (state == wait and
              event.timestamp() - t0 > args.tap_delay):
            state = tap
            tapToClick(True)
finally:
    # make sure tap is off when we leave
    tapToClick(False)
