"""Core slideshow functionality."""

import itertools
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


def iter_files(startdir, extensions=None):
    """Yield image files from the given directory using a generator."""
    if extensions is None:
        extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]

    def callback(filepath):
        filename, ext = os.path.splitext(filepath)
        e = ext.lower()
        if e in extensions:
            print(f"Found image: {filepath}")
            yield filepath
        else:
            print(f"Skipping: {filepath} (NOT a supported image)")

    for filepath in walktree_iter(startdir, callback):
        yield filepath


def walktree_iter(top, callback):
    """Generator version of walktree that yields files."""
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[stat.ST_MODE]
        if stat.S_ISDIR(mode):
            yield from walktree_iter(pathname, callback)
        elif stat.S_ISREG(mode):
            yield from callback(pathname)
        else:
            print(f"Skipping {pathname}")


def input_events(events):
    """A function to handle keyboard/mouse/device input events."""
    for event in events:  # Hit the ESC key to quit the slideshow.
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            return True
    return False


def run_slideshow(
    file_iter,
    title="pgSlideShow | My Slideshow!",
    waittime=1,
):
    """Run the slideshow with the given generator of image files."""
    pygame.init()

    if not pygame.image.get_extended():
        raise RuntimeError(
            "Your Pygame isn't built with extended image support. "
            "It's likely this isn't going to work."
        )

    file_cycle = itertools.cycle(file_iter)

    modes = pygame.display.list_modes()
    pygame.display.set_mode(max(modes))

    screen = pygame.display.get_surface()
    pygame.display.set_caption(title)
    pygame.display.toggle_fullscreen()

    running = True
    filepath = None

    while running:
        try:
            filepath = next(file_cycle)
            img = pygame.image.load(filepath)
            img = img.convert()
            img = pygame.transform.scale(img, max(modes))
            screen.blit(img, (0, 0))
            pygame.display.flip()

            if input_events(pygame.event.get()):
                running = False

            time.sleep(waittime)
        except StopIteration:
            raise ValueError("Sorry. No images found.")
        except pygame.error as err:
            print(f"Failed to display {filepath}: {err}")
