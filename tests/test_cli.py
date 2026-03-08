"""Tests for input_events and CLI functions."""

import argparse
from unittest.mock import MagicMock, patch

from pgslideshow import cli
from pgslideshow.slideshow import input_events


class TestInputEvents:
    """Tests for the input_events function."""

    @patch("pgslideshow.slideshow.QUIT", 1)
    @patch("pgslideshow.slideshow.KEYDOWN", 2)
    @patch("pgslideshow.slideshow.K_ESCAPE", 27)
    @patch("pgslideshow.slideshow.pygame")
    def test_input_events_returns_true_on_esc_key(self, mock_pygame):
        """input_events should return True when ESC key is pressed."""
        mock_event = MagicMock()
        mock_event.type = 2
        mock_event.key = 27

        result = input_events([mock_event])

        assert result is True
        mock_pygame.quit.assert_called_once()

    @patch("pgslideshow.slideshow.QUIT", 1)
    @patch("pgslideshow.slideshow.KEYDOWN", 2)
    @patch("pgslideshow.slideshow.K_ESCAPE", 27)
    @patch("pgslideshow.slideshow.pygame")
    def test_input_events_returns_true_on_quit(self, mock_pygame):
        """input_events should return True when QUIT event occurs."""
        mock_event = MagicMock()
        mock_event.type = 1

        result = input_events([mock_event])

        assert result is True
        mock_pygame.quit.assert_called_once()

    @patch("pgslideshow.slideshow.QUIT", 1)
    @patch("pgslideshow.slideshow.KEYDOWN", 2)
    @patch("pgslideshow.slideshow.K_ESCAPE", 27)
    @patch("pgslideshow.slideshow.pygame")
    def test_input_events_returns_false_no_events(self, mock_pygame):
        """input_events should return False when no relevant events."""
        mock_event = MagicMock()
        mock_event.type = 999

        result = input_events([mock_event])

        assert result is False
        mock_pygame.quit.assert_not_called()

    @patch("pgslideshow.slideshow.QUIT", 1)
    @patch("pgslideshow.slideshow.KEYDOWN", 2)
    @patch("pgslideshow.slideshow.K_ESCAPE", 27)
    @patch("pgslideshow.slideshow.pygame")
    def test_input_events_returns_false_other_key(self, mock_pygame):
        """input_events should return False for non-ESC keys."""
        mock_event = MagicMock()
        mock_event.type = 2
        mock_event.key = 65

        result = input_events([mock_event])

        assert result is False

    @patch("pgslideshow.slideshow.QUIT", 1)
    @patch("pgslideshow.slideshow.KEYDOWN", 2)
    @patch("pgslideshow.slideshow.K_ESCAPE", 27)
    @patch("pgslideshow.slideshow.pygame")
    def test_input_events_empty_list(self, mock_pygame):
        """input_events should return False for empty event list."""
        result = input_events([])

        assert result is False
        mock_pygame.quit.assert_not_called()


class TestCreateParser:
    """Tests for the create_parser function."""

    def test_create_parser_returns_argument_parser(self):
        """create_parser should return an ArgumentParser."""
        parser = cli.create_parser()

        assert isinstance(parser, argparse.ArgumentParser)

    def test_parser_has_path_argument(self):
        """Parser should have a positional path argument."""
        parser = cli.create_parser()

        args = parser.parse_args(["/some/path"])

        assert args.path == "/some/path"

    def test_parser_default_path_is_current_dir(self):
        """Parser should default path to current directory."""
        parser = cli.create_parser()

        args = parser.parse_args([])

        assert args.path == "."

    def test_parser_has_waittime_argument(self):
        """Parser should have a --waittime argument."""
        parser = cli.create_parser()

        args = parser.parse_args([".", "--waittime", "5"])

        assert args.waittime == 5

    def test_parser_default_waittime(self):
        """Parser should default waittime to 1."""
        parser = cli.create_parser()

        args = parser.parse_args([])

        assert args.waittime == 1

    def test_parser_has_title_argument(self):
        """Parser should have a --title argument."""
        parser = cli.create_parser()

        args = parser.parse_args([".", "--title", "My Custom Title"])

        assert args.title == "My Custom Title"

    def test_parser_default_title(self):
        """Parser should have a default title."""
        parser = cli.create_parser()

        args = parser.parse_args([])

        assert args.title == "pgSlideShow | My Slideshow!"

    def test_parser_all_arguments_together(self):
        """Parser should accept all arguments together."""
        parser = cli.create_parser()

        args = parser.parse_args(
            ["/path/to/images", "--waittime", "3", "--title", "Test Slideshow"]
        )

        assert args.path == "/path/to/images"
        assert args.waittime == 3
        assert args.title == "Test Slideshow"


class TestMain:
    """Tests for the main CLI function."""

    def test_main_calls_iter_files_and_run_slideshow(self):
        """main should call iter_files and run_slideshow."""
        with patch("pgslideshow.cli.iter_files") as mock_iter_files, patch(
            "pgslideshow.cli.run_slideshow"
        ) as mock_run:
            mock_iter_files.return_value = iter(["/path/to/image.png"])

            cli.main(["/some/path"])

            mock_iter_files.assert_called_once_with("/some/path")
            mock_run.assert_called_once()

    def test_main_with_custom_waittime(self):
        """main should pass custom waittime to run_slideshow."""
        with patch("pgslideshow.cli.iter_files") as mock_iter_files, patch(
            "pgslideshow.cli.run_slideshow"
        ) as mock_run:
            mock_iter_files.return_value = iter(["/path/to/image.png"])

            cli.main([".", "--waittime", "5"])

            mock_run.assert_called_once()
            _, kwargs = mock_run.call_args
            assert kwargs["waittime"] == 5

    def test_main_with_custom_title(self):
        """main should pass custom title to run_slideshow."""
        with patch("pgslideshow.cli.iter_files") as mock_iter_files, patch(
            "pgslideshow.cli.run_slideshow"
        ) as mock_run:
            mock_iter_files.return_value = iter(["/path/to/image.png"])

            cli.main([".", "--title", "Custom Title"])

            mock_run.assert_called_once()
            _, kwargs = mock_run.call_args
            assert kwargs["title"] == "Custom Title"

    def test_main_keyboard_interrupt(self):
        """main should handle KeyboardInterrupt gracefully."""
        with patch("pgslideshow.cli.iter_files") as mock_iter_files:
            mock_iter_files.side_effect = KeyboardInterrupt()

            with patch("sys.exit") as mock_exit:
                cli.main(["."])

                mock_exit.assert_called_once_with(0)

    def test_main_general_exception(self):
        """main should handle general exceptions and exit with code 1."""
        with patch("pgslideshow.cli.iter_files") as mock_iter_files:
            mock_iter_files.side_effect = RuntimeError("Some error")

            with patch("sys.exit") as mock_exit:
                cli.main(["."])

                mock_exit.assert_called_once_with(1)
