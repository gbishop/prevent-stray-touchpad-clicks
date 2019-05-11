# prevent-stray-touchpad-clicks

Prevent stray clicks on my XPS 13 touchpad by enabling tap-to-click only after
a period of pad activity.

The touchpad on my Dell XPS 13 Developer Edition drives me crazy by registering
stray clicks when my hands come too near while typing. I've seen a few applications
intended to help with this by disabling the touchpad during typing. They didn't
do the job for me. I found that it doesn't only happen while typing is underway
but often just as I start to type. 

I reasoned that a better strategy would be to monitor the touchpad and only enable
tap-to-click after a short period of activity. How often is the cursor exactly
where you want it and all you need to do is swoop in and tap the pad? Never for me.
The more common scenerio is I slide my finger on the pad to get the cursor to the 
correct spot and then tap. 

With this script the touchpad is always enabled and actually clicking always works;
I'm only controlling the `tap-to-click` flag.

I access the Linux /dev/input/eventN interface using the
[evdev](https://python-evdev.readthedocs.io/en/latest/) module to monitor the
touchpad and
[gsettings](http://manpages.ubuntu.com/manpages/bionic/man1/gsettings.1.html)
to control `tap-to-click`. I had to add myself to the `input` group to get
access to the device.

I start it from `Startup Applications`.
