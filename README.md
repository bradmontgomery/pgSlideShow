# pgSlideShow

pgSlideShow is an image slideshow application written in Python using [pygame](https://www.pygame.org/).
It recursively searches a given directory for image files, and then displays
them in Fullscreen mode. Images are currently resized to fit the screen,
so some pixelization may occur.

**Note**: this code aims for simplicity over performance. The initial search for
image files is slow and probably takes up more memory than it should.

## Requirements

You need to have pygame installed. See the [pygame installation docs](https://www.pygame.org/wiki/GettingStarted).

## Installation

Using [uv](https://docs.astral.sh/uv/):

```bash
uv pip install -e .
```

## Usage

This is a command-line application. To run it, type the following command,
specifying the path to the directory in which your images are located.

If no directory is given, pgSlideShow will recursively search for images in
the current directory.

```bash
python -m pgslideshow [directory]
```

Or, if installed:

```bash
pgslideshow [directory]
```

### Command-line Options

Run `pgslideshow -h` for more details:

- `--waittime`: Time to wait between images (seconds, default: 1)
- `--title`: Set the window title
- `--help`: Show help message

## History

This was written back in 2007 when I first started tinkering with pygame. See
[this blog post](https://bradmontgomery.net/blog/2007/10/31/announcing-pgslideshow/).

## License

This code is available under the [MIT License](LICENSE.md).
