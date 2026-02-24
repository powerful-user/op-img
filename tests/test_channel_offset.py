"""Tests for channel-offset tool (ImageMagick)."""

import pytest

from conftest import assert_valid_image, skip_without_imagemagick

pytestmark = pytest.mark.imagemagick


@skip_without_imagemagick()
class TestChannelOffset:
    def test_default_args(self, run_tool, tmp_workdir):
        tmp_path, img = tmp_workdir
        r = run_tool("channel-offset", "channel-offset.sh", [img])
        assert r.returncode == 0
        out = str(tmp_path / "input-offset.png")
        assert_valid_image(out)

    def test_explicit_options(self, run_tool, tmp_workdir):
        tmp_path, img = tmp_workdir
        out = str(tmp_path / "offset.png")
        r = run_tool("channel-offset", "channel-offset.sh", [
            img, out, "--r", "5,0", "--g", "0,0", "--b", "-5,0",
        ])
        assert r.returncode == 0
        assert_valid_image(out)
        assert "r:5,0" in r.stderr

    def test_missing_input(self, run_tool):
        r = run_tool("channel-offset", "channel-offset.sh", ["/nonexistent/image.png"])
        assert r.returncode != 0
        assert "not found" in r.stderr.lower()

    def test_no_args(self, run_tool):
        r = run_tool("channel-offset", "channel-offset.sh", [])
        assert r.returncode != 0
        assert "Usage:" in r.stderr
