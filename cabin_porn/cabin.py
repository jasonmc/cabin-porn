#!/usr/bin/env python

'''
Sets the current screen to a cabin from CabinPorn.com.

Default is set to the most recent picture, which it downloads.

Uses code to set desktop pictures for all screens from:
https://github.com/grahamgilbert/macscripts/tree/master/set_desktops
'''
import errno
import json
import os.path
import platform
import random
import requests
from PIL import Image
from optparse import OptionParser


url = "https://api.tumblr.com/v2/blog/cabinporn.com/posts/photo"\
      "?api_key=sZWRBqPLBfUJAsRY2Obu5SSioiwJasR0YGcgP5MSYulnQfpZyi"


def setBackgroundOSX(fullPath):
    from AppKit import NSWorkspace, NSScreen
    from Foundation import NSURL
    # generate a fileURL for the desktop picture
    file_path = NSURL.fileURLWithPath_(fullPath)
    # get shared workspace
    ws = NSWorkspace.sharedWorkspace()
    # iterate over all screens
    for screen in NSScreen.screens():
        # tell the workspace to set the desktop picture
        (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
            file_path, screen, {}, None)

def setBackgroundGnome(fullPath):
    from gi.repository import Gio
    SCHEMA = 'org.gnome.desktop.background'
    KEY = 'picture-uri'
    gsettings = Gio.Settings.new(SCHEMA)
    gsettings.set_string(KEY, "file://" + fullPath)

def createDirIfNotExists(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def directoryToSave():
    return os.path.join(os.path.expanduser("~/Pictures/cabins"))

def getPhotoUrls():
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        posts = data['response']['posts']
        return ((p['slug'], p['photos'][0]['original_size']['url'])
                for p in posts)
    else:
        return iter(())

def downloadImageIfNotExists(url, path):
    if not os.path.isfile(path):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

def detectOSAndSetBackground(fullPath):
    if platform.system() == "Linux":
        setBackgroundGnome(fullPath)
    elif platform.system() == "Darwin":
        setBackgroundOSX(fullPath)
    else:
        print("Not supported on this platform")

def meetsSizeRequirements(fullPath):
    width, height = Image.open(fullPath).size
    return width >= 1024 and height >= 768

def main():
    defaultPath = os.path.join(os.path.expanduser("~/Pictures/cabins"))
    parser = OptionParser()
    parser.add_option("-r", "--random", action="store_true",
                      dest="random_cabin", default=False,
                      help="pick a random cabin")
    parser.add_option("-l", "--large-only", dest="large_only",
                      help="only use large images", default=False,
                      action="store_true")
    parser.add_option("-p", "--path", dest="base_dir",
                      help="write cabins to PATH", metavar="PATH",
                      default=defaultPath)
    options, _ = parser.parse_args()

    createDirIfNotExists(base_dir)
    slug, url = (random.choice(list(getPhotoUrls()))
                 if options.random_cabin
                 else getPhotoUrls().next())
    fullPath = os.path.join(base_dir, slug + os.path.splitext(url)[1])
    downloadImageIfNotExists(url, fullPath)
    if not options.large_only or meetsSizeRequirements(fullPath):
        detectOSAndSetBackground(fullPath)

if __name__ == "__main__":
    main()
