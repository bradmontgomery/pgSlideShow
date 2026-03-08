"""Pytest fixtures for pgSlideShow tests."""


import pytest


@pytest.fixture
def temp_image_dir(tmp_path):
    """Create a temporary directory with image files for testing."""
    (tmp_path / "image1.png").touch()
    (tmp_path / "image2.jpg").touch()
    (tmp_path / "image3.jpeg").touch()
    (tmp_path / "image4.gif").touch()
    (tmp_path / "image5.bmp").touch()
    (tmp_path / "not_an_image.txt").touch()
    return tmp_path


@pytest.fixture
def nested_image_dir(tmp_path):
    """Create a nested directory structure with image files."""
    subdir1 = tmp_path / "subdir1"
    subdir2 = tmp_path / "subdir2"
    subdir1.mkdir()
    subdir2.mkdir()

    (tmp_path / "root.png").touch()
    (subdir1 / "nested1.jpg").touch()
    (subdir2 / "nested2.gif").touch()
    (subdir1 / "nested3.bmp").touch()

    return tmp_path


@pytest.fixture
def empty_dir(tmp_path):
    """Create an empty temporary directory."""
    return tmp_path


@pytest.fixture
def dir_with_subdirs_only(tmp_path):
    """Create a directory with only subdirectories (no files)."""
    (tmp_path / "subdir1").mkdir()
    (tmp_path / "subdir2").mkdir()
    return tmp_path


@pytest.fixture
def mixed_extensions_dir(tmp_path):
    """Create a directory with various file extensions."""
    image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
    other_extensions = [".txt", ".doc", ".pdf", ".py", ".JPG", ".PNG", ".GIF"]

    for ext in image_extensions:
        (tmp_path / f"file{ext}").touch()

    for ext in other_extensions:
        (tmp_path / f"file{ext}").touch()

    return tmp_path
