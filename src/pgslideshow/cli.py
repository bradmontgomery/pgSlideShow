"""Command-line interface for pgSlideShow."""

import argparse
import sys

from .slideshow import build_file_list, run_slideshow


def create_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Recursively loads images "
        "from a directory, then displays them in a Slideshow."
    )

    parser.add_argument(
        "path",
        metavar="ImagePath",
        type=str,
        default=".",
        nargs="?",
        help="Path to a directory that contains images",
    )
    parser.add_argument(
        "--waittime",
        type=int,
        dest="waittime",
        action="store",
        default=1,
        help="Amount of time to wait before showing the next image.",
    )
    parser.add_argument(
        "--title",
        type=str,
        dest="title",
        action="store",
        default="pgSlideShow | My Slideshow!",
        help="Set the title for the display window.",
    )

    return parser


def main(args=None):
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    try:
        # Build the list of image files
        file_list = build_file_list(parsed_args.path)

        # Run the slideshow
        run_slideshow(
            file_list=file_list,
            title=parsed_args.title,
            waittime=parsed_args.waittime,
        )
    except KeyboardInterrupt:
        print("\nSlideshow interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
