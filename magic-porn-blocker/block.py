from tkinter import *

from python_hosts import Hosts, HostsEntry

from elevate import elevate

import os
import sys
import re
import threading
import tempfile


# Ask for administrator permissions
elevate(show_console=True)


"""
----------------------------------------------------
BLOCK
----------------------------------------------------
"""

# Read the filtered blocklist
os.chdir(tempfile.gettempdir())
f = open("porn.filtered.blocklist", "r")
data = f.read()
data = data.split('\n')

# Starts the block() function as a new thread
def threadBlock():
    threading.Thread(target=block).start()

def block():

    # Remove previous blocks to prevent duplicates
    progress.set( "Processing hosts file" )
    if sys.platform.startswith("win"):
        path = "C:\Windows\System32\drivers\etc\hosts"
    else:
        path = "/etc/hosts"
    hosts = Hosts(path)
    hosts.remove_all_matching(address="0.0.0.1")
    hosts.write()

    # Add domains to hosts file with IP 0.0.0.1
    # 8 domains in a row (hosts file limitation)
    # https://superuser.com/questions/932112/is-there-a-maxium-number-of-hostname-aliases-per-line-in-a-windows-hosts-file
    for i in range(0, len(data), 8):
        new_entry = HostsEntry(entry_type='ipv4', address='0.0.0.1', names=data[i:(i+8)])
        hosts.add([new_entry], False, True)
        progress.set( str( round(100*i/len(data),2)) + "%" )
    hosts.write()

    progress.set( "100 %" )
    status.set("DONE (You can close the program. Restart your browser.)")


"""
----------------------------------------------------
GUI
----------------------------------------------------
"""

# Basic settings
window = Tk()
window.title = "Blocking in progress..."
window.configure(background="black")
window.minsize(500,100)
window.geometry("500x100")
window.grid_columnconfigure(0, weight=1)
col_count, row_count = window.grid_size()
for row in range(row_count):
    window.grid_rowconfigure(row, minsize=300)


# Block progress
progress = StringVar()
Label(window, text="Blocking in progress, please wait...", bg="black", fg="gray", font="Courier 16" ) .grid(row=0, column=0)
Label(window, textvariable=progress, bg="black", fg="white", font="Courier 16" ) .grid(row=1, column=0)
progress.set( "0 %" )

# Status
status = StringVar()
Label(window, textvariable=status, bg="black", fg="green", font="none 14 bold" ) .grid(row=11, column=0)

# Start block
threadBlock()

window.mainloop()

