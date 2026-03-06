# pgSlideShow

A pygame-based image slideshow application.

## Overview

1. Recursively scan a directory for image files (png, jpg, jpeg, gif, bmp)
2. Use Python generators to yield files one at a time (memory-efficient)
3. Display images in a fullscreen pygame window, cycling indefinitely

## Project Structure

```
src/pgslideshow/
├── __init__.py       # Package init
├── __main__.py       # Module entry point
├── cli.py            # Command-line interface with argparse
└── slideshow.py      # Core slideshow logic (generators, pygame rendering)
```

## Quick Start

```bash
# Install in development mode
uv pip install -e .

# Run the slideshow
python -m pgslideshow [directory]
```

## Key Patterns

- **Generators**: Use `iter_files()` and `walktree_iter()` for lazy file discovery
- **Infinite iteration**: `itertools.cycle()` wraps the generator for looping
- **pygame display**: Fullscreen mode with `pygame.transform.scale` to fit screen

## Testing

Run tests with `pytest` (if available in the environment).

## Git Commits

Append `Co-authored-by` annotations for OpenCode usage:

```
Co-authored-by: Kimi-K2.5 <Kimi-K2.5@opencode.ai>
Co-authored-by: Qwen3.5:2b <qwen3.5-2b@ollama.localhost>
```
