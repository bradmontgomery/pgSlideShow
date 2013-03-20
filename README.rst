pgSlideShow
===========

pgSlideShow is an image slideshow application written in Python using pygame.
It recursively searches a given directory for image files, and then displays
them in Fullscreen mode. Images are currently resized to fit the screen,
so some pixelization may occur.


Usage
-----

python pgSlideShow.py [directory]
pgSlideShow is a command-line application. To run it, simply type the command above, specifying the path to the directory in which your images are located. If no directory is given, pgSlideShow will recursively search for images in the directory from which it is run.

History
-------

This was written back in 2007 when I first started tinkering with pygame. See
`this blog post <https://bradmontgomery.net/blog/2007/10/31/announcing-pgslideshow/>`_.

License
-------

This code is available under the MIT License.
