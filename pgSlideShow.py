"""
A pygame program to show a slideshow of all images buried in a given directory.

Released: 2007.10.31 (Happy halloween!)

"""
import os
import stat
import sys
import time

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

file_list = []  # a list of all images being shown
title = "pgSlideShow | My Slideshow!"  # caption of the window...
waittime = 1   # how long to wait between images (in seconds)


def walktree(top, callback):
    """recursively descend the directory tree rooted at top, calling the
    callback function for each regular file. Taken from the module-stat
    example at: http://docs.python.org/lib/module-stat.html
    """
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[stat.ST_MODE]
        if stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif stat.S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname


def addtolist(file, extensions=['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
    """Add a file to a global list of image files."""
    global file_list  # ugh
    filename, ext = os.path.splitext(file)
    e = ext.lower()
    # Only add common image types to the list.
    if e in extensions:
        print 'Adding to list: ', file
        file_list.append(file)
    else:
        print 'Skipping: ', file, ' (NOT a supported image)'


def input(events):
    """A function to handle keyboard/mouse/device input events. """
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()


def main(startdir="."):
    global file_list, title, waittime

    walktree(startdir, addtolist)  # this may take a while...
    pygame.init()

    modes = pygame.display.list_modes()
    pygame.display.set_mode(max(modes))

    screen = pygame.display.get_surface()
    pygame.display.set_caption(title)
    pygame.display.toggle_fullscreen()

    current = 0
    num_files = len(file_list)
    while(True):
        img = pygame.image.load(file_list[current])
        img = img.convert()
        # rescale the image to fit the current display
        img = pygame.transform.scale(img, max(modes))
        screen.blit(img, (0, 0))
        pygame.display.flip()
        if current == num_files - 1:
            current = 0  # loop the slideshow
        else:
            current = current + 1
        input(pygame.event.get())
        time.sleep(waittime)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
