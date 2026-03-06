"""Core slideshow functionality."""

import os
import stat
import time

import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT


def walktree(top, callback):
    """Recursively descend the directory tree rooted at top, calling the
    callback function for each regular file. Based on the module-stat
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
            print(f"Skipping {pathname}")


def addtolist(file, extensions=None):
    """Add a file to a global list of image files."""
    if extensions is None:
        extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]

    filename, ext = os.path.splitext(file)
    e = ext.lower()
    # Only add common image types to the list.
    if e in extensions:
        print(f"Adding to list: {file}")
        return file
    else:
        print(f"Skipping: {file} (NOT a supported image)")
        return None


def build_file_list(startdir, extensions=None):
    """Build a list of image files from the given directory."""
    file_list = []

    def callback(filepath):
        result = addtolist(filepath, extensions)
        if result:
            file_list.append(result)

    walktree(startdir, callback)
    return file_list


def input_events(events):
    """A function to handle keyboard/mouse/device input events."""
    for event in events:  # Hit the ESC key to quit the slideshow.
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            return True
    return False


def run_slideshow(
    file_list,
    title="pgSlideShow | My Slideshow!",
    waittime=1,
):
    """Run the slideshow with the given list of image files."""
    pygame.init()

    # Test for image support
    if not pygame.image.get_extended():
        raise RuntimeError(
            "Your Pygame isn't built with extended image support. "
            "It's likely this isn't going to work."
        )

    if len(file_list) == 0:
        raise ValueError("Sorry. No images found.")

    modes = pygame.display.list_modes()
    pygame.display.set_mode(max(modes))

    screen = pygame.display.get_surface()
    pygame.display.set_caption(title)
    pygame.display.toggle_fullscreen()

    current = 0
    num_files = len(file_list)
    running = True

    while running:
        try:
            img = pygame.image.load(file_list[current])
            img = img.convert()
            # rescale the image to fit the current display
            img = pygame.transform.scale(img, max(modes))
            screen.blit(img, (0, 0))
            pygame.display.flip()

            if input_events(pygame.event.get()):
                running = False

            time.sleep(waittime)
        except pygame.error as err:
            print(f"Failed to display {file_list[current]}: {err}")

        # When we get to the end, re-start at the beginning
        current = (current + 1) % num_files
