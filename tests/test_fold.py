"""Tests for fold tool (ImageMagick)."""

import pytest

from conftest import assert_valid_image, skip_without_imagemagick

pytestmark = pytest.mark.imagemagick


@skip_without_imagemagick()
class TestFold:
    def test_default_args(self, run_tool, tmp_workdir):
        tmp_path, img = tmp_workdir
        r = run_tool("fold", "fold.sh", [img])
        assert r.returncode == 0
        out = str(tmp_path / "input-fold.png")
        assert_valid_image(out)

    def test_y_axis_repeat(self, run_tool, tmp_workdir):
        tmp_path, img = tmp_workdir
        out = str(tmp_path / "folded.png")
        r = run_tool("fold", "fold.sh", [
            img, out, "--axis", "y", "--mode", "repeat",
        ])
        assert r.returncode == 0
        assert_valid_image(out)

    def test_invalid_axis(self, run_tool, tmp_workdir):
        _, img = tmp_workdir
        r = run_tool("fold", "fold.sh", [img, "--axis", "z"])
        assert r.returncode != 0
        assert "x or y" in r.stderr.lower()

    def test_missing_input(self, run_tool):
        r = run_tool("fold", "fold.sh", ["/nonexistent/image.png"])
        assert r.returncode != 0
        assert "not found" in r.stderr.lower()

    def test_no_args(self, run_tool):
        r = run_tool("fold", "fold.sh", [])
        assert r.returncode != 0
        assert "Usage:" in r.stderr
