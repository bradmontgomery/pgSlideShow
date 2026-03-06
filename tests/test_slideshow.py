"""Tests for the slideshow module."""

import os

from pgslideshow.slideshow import (
    iter_files,
    walktree,
    walktree_iter,
)


class TestWalktree:
    """Tests for the original walktree function."""

    def test_walktree_finds_all_files(self, temp_image_dir):
        """walktree should find all files in directory."""
        files = []

        def callback(filepath):
            files.append(filepath)

        walktree(str(temp_image_dir), callback)

        assert len(files) == 6

    def test_walktree_finds_nested_files(self, nested_image_dir):
        """walktree should recursively find files in subdirectories."""
        files = []

        def callback(filepath):
            files.append(filepath)

        walktree(str(nested_image_dir), callback)

        assert len(files) == 4

    def test_walktree_handles_empty_dir(self, empty_dir):
        """walktree should handle empty directories."""
        files = []

        def callback(filepath):
            files.append(filepath)

        walktree(str(empty_dir), callback)

        assert files == []


class TestWalktreeIter:
    """Tests for the walktree_iter generator function."""

    def test_walktree_iter_yields_files(self, temp_image_dir):
        """walktree_iter should yield files as a generator."""
        results = list(walktree_iter(str(temp_image_dir), lambda x: [x]))

        assert len(results) == 6

    def test_walktree_iter_nested_directories(self, nested_image_dir):
        """walktree_iter should recursively yield files from subdirectories."""
        results = list(walktree_iter(str(nested_image_dir), lambda x: [x]))

        assert len(results) == 4

    def test_walktree_iter_empty_directory(self, empty_dir):
        """walktree_iter should handle empty directories."""
        results = list(walktree_iter(str(empty_dir), lambda x: [x]))

        assert results == []

    def test_walktree_iter_only_subdirs(self, dir_with_subdirs_only):
        """walktree_iter should handle directories with only subdirectories."""
        results = list(walktree_iter(str(dir_with_subdirs_only), lambda x: [x]))

        assert results == []

    def test_walktree_iter_is_generator(self, temp_image_dir):
        """walktree_iter should return a generator object."""
        result = walktree_iter(str(temp_image_dir), lambda x: [x])

        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_walktree_iter_with_filtering(self, mixed_extensions_dir):
        """walktree_iter should work with callback filtering."""

        def filter_images(path):
            ext = os.path.splitext(path)[1].lower()
            if ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]:
                return [path]
            return []

        results = list(walktree_iter(str(mixed_extensions_dir), filter_images))

        # 5 lowercase + 3 uppercase image extensions
        assert len(results) == 8


class TestIterFiles:
    """Tests for the iter_files generator function."""

    def test_iter_files_finds_images(self, temp_image_dir):
        """iter_files should yield only image files."""
        results = list(iter_files(str(temp_image_dir)))

        assert len(results) == 5

    def test_iter_files_skips_non_images(self, temp_image_dir):
        """iter_files should skip non-image files."""
        results = list(iter_files(str(temp_image_dir)))

        for filepath in results:
            assert not filepath.endswith("txt")

    def test_iter_files_nested_directories(self, nested_image_dir):
        """iter_files should find images in nested directories."""
        results = list(iter_files(str(nested_image_dir)))

        assert len(results) == 4

    def test_iter_files_empty_directory(self, empty_dir):
        """iter_files should handle empty directories."""
        results = list(iter_files(str(empty_dir)))

        assert results == []

    def test_iter_files_only_subdirs(self, dir_with_subdirs_only):
        """iter_files should handle directories with only subdirectories."""
        results = list(iter_files(str(dir_with_subdirs_only)))

        assert results == []

    def test_iter_files_case_insensitive(self, tmp_path):
        """iter_files should be case-insensitive for extensions."""
        (tmp_path / "test.PNG").touch()
        (tmp_path / "test.JPG").touch()
        (tmp_path / "test.GIF").touch()

        results = list(iter_files(str(tmp_path)))

        assert len(results) == 3

    def test_iter_files_custom_extensions(self, tmp_path):
        """iter_files should accept custom extensions."""
        (tmp_path / "test.txt").touch()
        (tmp_path / "test.csv").touch()

        results = list(iter_files(str(tmp_path), extensions=[".txt", ".csv"]))

        assert len(results) == 2

    def test_iter_files_is_generator(self, temp_image_dir):
        """iter_files should return a generator."""
        result = iter_files(str(temp_image_dir))

        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_iter_files_all_supported_extensions(self, tmp_path):
        """iter_files should find all supported image extensions."""
        extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
        for ext in extensions:
            (tmp_path / f"image{ext}").touch()

        results = list(iter_files(str(tmp_path)))

        assert len(results) == 5
