pgSlideShow
===========

pgSlideShow is an image slideshow application written in Python using pygame.
It recursively searches a given directory for image files, and then displays
them in Fullscreen mode. Images are currently resized to fit the screen,
so some pixelization may occur.

*Note*: this code aims for simplicity over performance. The inital search for
image files is slow and probably takes up more memory than it should.


Requirements
------------

You need to have pygame installed and on your python path, and it needs to have
been built with with full image support, otherwise it will not be able to load
most image formats. See [the pygame.image](http://www.pygame.org/docs/ref/image.html) docs.

Usage
-----

This is a command-line application. To run it, type the following command,
specifying the path to the directory in which your images are located.

If no directory is given, pgSlideShow will recursively search for images in
the directory from which it is run.

::

    python src/pgSlideShow.py [directory]


History
-------

This was written back in 2007 when I first started tinkering with pygame. See
`this blog post <https://bradmontgomery.net/blog/2007/10/31/announcing-pgslideshow/>`_.

License
-------

This code is available under the MIT License.
