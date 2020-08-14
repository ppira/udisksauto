#!/usr/bin/python3

import subprocess
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib, GObject
DBusGMainLoop(set_as_default=True)
 
bus = dbus.SystemBus()
 
def callback_function(objectpath, interfaces):
    if not str(objectpath).startswith('/org/freedesktop/UDisks2/block_devices/'):
        return
    try:
        obj = bus.get_object('org.freedesktop.UDisks2', objectpath)
        iface = dbus.Interface(obj, 'org.freedesktop.UDisks2.Filesystem')
        path = iface.get_dbus_method('Mount', dbus_interface='org.freedesktop.UDisks2.Filesystem')({'options': 'ro'})
    except dbus.exceptions.DBusException:
        return
    except ValueError:
        return
 
signal = 'InterfacesAdded'
iface  = 'org.freedesktop.DBus.ObjectManager'
bus.add_signal_receiver(callback_function, signal, iface)

loop = GObject.MainLoop()
loop.run()
