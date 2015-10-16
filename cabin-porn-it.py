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
import random
import requests
from AppKit import NSWorkspace, NSScreen
from Foundation import NSURL
from PIL import Image
from optparse import OptionParser


url = "https://api.tumblr.com/v2/blog/cabinporn.com/posts/photo"\
      "?api_key=sZWRBqPLBfUJAsRY2Obu5SSioiwJasR0YGcgP5MSYulnQfpZyi"


def setBackgroundOSX(fullPath):
    # generate a fileURL for the desktop picture
    file_path = NSURL.fileURLWithPath_(fullPath)
    # get shared workspace
    ws = NSWorkspace.sharedWorkspace()
    # iterate over all screens
    for screen in NSScreen.screens():
        # tell the workspace to set the desktop picture
        (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
            file_path, screen, {}, None)


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


def main():
    parser = OptionParser()
    parser.add_option("-r", "--random", action="store_true",
                      dest="random_cabin", default=False,
                      help="pick a random cabin")
    options, _ = parser.parse_args()

    saveDir = directoryToSave()
    createDirIfNotExists(saveDir)
    slug, url = (random.choice(list(getPhotoUrls()))
                 if options.random_cabin
                 else getPhotoUrls().next())
    fullPath = os.path.join(saveDir, slug + os.path.splitext(url)[1])
    downloadImageIfNotExists(url, fullPath)
    width, height = Image.open(fullPath).size
    if width >= 1024 and height >= 768:
        setBackgroundOSX(fullPath)

if __name__ == "__main__":
    main()
