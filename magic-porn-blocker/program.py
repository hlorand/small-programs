#!/usr/bin/env python3

production_build = True

"""
Magic porn blocker

This program blocks all adult themed websites using your system's hosts file.
The URL blacklist downloaded from https://blocklist.site

Usage: python3 program.py

Build with:
- OSX: py2app
- Win: pyinstaller
"""

__author__ = "Lorand Horvath"
__copyright__ = "Copyright 2019, hlorand.hu"
__license__ = "https://choosealicense.com/licenses/gpl-3.0/"
__version__ = "0.1"
__email__ = "email at hlorand dot hu"

"""
------------------------------------------------
IMPORTS
----------------------------------------------------
"""

from tkinter import *
from urllib.request import *

import ssl
import threading
import platform
import os
import sys
import re
import subprocess
import math
import tempfile

"""
----------------------------------------------------
DOWNLOAD

Downloads the blocklist from blocklist.site
----------------------------------------------------
"""

# Updates the progress label
def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100)
   mbytes_so_far = math.ceil(bytes_so_far / 1024 / 1024)
   mtotal_size = math.ceil(total_size / 1024 / 1024)
   progress.set("Downloaded " +str(mbytes_so_far)+ " of " +str(mtotal_size)+ " MB (" +str(percent)+ "%)" )

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')

# Reads the data and combines the chunks into a file
def chunk_read(response, chunk_size=8192, report_hook=None):
   total_size = response.getheader('Content-Length').strip()
   total_size = int(total_size)
   bytes_so_far = 0
   data = bytearray(b'')

   while 1:
      chunk = response.read(chunk_size)
      data.extend(chunk)
      bytes_so_far += len(chunk)

      if not chunk:
         break

      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)

   os.chdir(tempfile.gettempdir())
   f = open("porn.blocklist", "w")
   f.write(data.decode("utf-8"))
   f.close()
   
   return

# Starts the download() function as a new thread
def threadDownload():
    threading.Thread(target=download).start()

def download():

   scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
   user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
   headers={'User-Agent':user_agent,}
   
   # More info: https://blocklist.site/app/list-details.php?list=porn
   if production_build:
      url = "https://blocklist.site/app/dl/porn" 
   else:
      url = "https://blocklist.site/app/dl/proxy" # shorter list for testing purposes
   
   request = Request(url, None, headers)
   response = urlopen(request, context=scontext)
   data = chunk_read(response, report_hook=chunk_report)

   # Filter the downloaded data
   filterlist()

"""
----------------------------------------------------
FILTER BLOCKLIST

Removes IP addresses and subdomains from the list
making it lighter to prevent a huge hosts file.

Modify the domain length below to make it even shorter.
----------------------------------------------------
"""
def filterlist():

    print("Filtering strarted")

    os.chdir(tempfile.gettempdir())
    f = open("porn.blocklist", "r")
    data = f.read()
    data = data.split('\n')

    # remove empty lines
    data = list(filter(None, data))

    # remove duplicates
    data = list(dict.fromkeys(data))

    fout = open("porn.filtered.blocklist", "w")

    length = len(data)

    count = 0
    for element in data:
        count = count + 1

        try:
            # remove ip addresses
            if re.sub('[.]', '', element).isnumeric():
                continue
            
            # remove subdomains
            if element.count('.') > 1:
                continue

            # remove long domains
            if len(element) > 20:
                continue

            progress.set("Processing " +str(round(length/1000000,2))+ " million websites (" +str( round(100*count/len(data),2) )+ "%)" )

            fout.write(element + "\n")
            
        except ValueError:
            pass

    fout.close()

    progress.set("Download succeeded proceed to step 2" )
    print("Filtering ended")

    return

"""
----------------------------------------------------
BLOCK

Starts the block.py which blocks the sites.

Needed to place this into a separate file
because the privilege elevation restarts the
script and you can't do this with the main program,
only with a subprocess.
----------------------------------------------------
"""
def block():
   print("Starting block.py")

   # py2app (on OSX) messes up the path variable, these lines fix
   # the path where block.py located. 
   if sys.platform.startswith("win") or not production_build:
      path = sys.path[0]
   else:
      path = sys.path[0].split("/lib/",1)[0]

   os.chdir(path)
   
   command = sys.executable + " -u block.py"
   subprocess.Popen(command, shell=True)

"""
----------------------------------------------------
GUI
----------------------------------------------------
"""

# Basic settings
window = Tk()
window.title = "Magic Porn Blocker"
window.configure(background="black")
if sys.platform.startswith("win"):
    window.minsize(600,550)
    window.geometry("600x550")
else:
    window.minsize(600,420)
    window.geometry("600x420")
window.grid_columnconfigure(0, weight=1)
col_count, row_count = window.grid_size()
for row in range(row_count):
    window.grid_rowconfigure(row, minsize=300)

# Logo image
mpb_logo = PhotoImage(file="mpb_logo.png")
Label(window, image=mpb_logo, bg="black") .grid(row=0, column=0)

# Description
Label(window, wraplength=550, text="The program blocks all adult themed websites. First download the blocklist from TheBlocklistProject website (www.blocklist.site) then click on the block button. The program will ask for administrator permissions.", bg="black", fg="gray", font="none 16" ) .grid(row=1, column=0)

# Step 1: Download
Label(window, text="STEP 1", bg="black", fg="white", font="none 20 bold" ) .grid(row=2, column=0)
Button(window, text="DOWNLOAD BLOCK LIST", width=20, highlightbackground="white", command=threadDownload, font="none 18 bold" ) .grid(row=3, column=0)

# Download progress
progress = StringVar()
Label(window, textvariable=progress, bg="black", fg="gray", font="Courier 16" ) .grid(row=4, column=0)

# Choose block length
# TODO: Implement
"""
Label(window, text="STEP 2: Choose block length", bg="black", fg="white", font="none 20 bold" ) .grid(row=5, column=0)
Button(window, text="1 day", width=10, highlightbackground="green", command=download, font="none 18 bold" ) .grid(row=6, column=0)
Button(window, text="1 week", width=10, highlightbackground="orange", command=download, font="none 18 bold" ) .grid(row=7, column=0)
"""

# Step 2: Block
Label(window, text="STEP 2", bg="black", fg="white", font="none 20 bold" ) .grid(row=8, column=0)
Button(window, text="BLOCK FOREVER", width=20, highlightbackground="red", command=block, font="none 30 bold" ) .grid(row=9, column=0)

# Unblock button - hidden outside of the main window edges (pull bottom edge down to show)
# TODO: Implement
Label(window, text=" ", bg="black", fg="white", font="none 50 bold" ) .grid(row=10, column=0) #just a spacer
Button(window, text="Unblock (You don't want this)", width=20, highlightbackground="green", command=block, font="none 10 bold" ) .grid(row=11, column=0)


window.mainloop()
