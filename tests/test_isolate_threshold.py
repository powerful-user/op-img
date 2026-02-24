"""Tests for isolate-threshold tool (ImageMagick)."""

import pytest

from conftest import assert_valid_image, skip_without_imagemagick

pytestmark = pytest.mark.imagemagick


@skip_without_imagemagick()
class TestIsolateThreshold:
    def test_default_args(self, run_tool, tmp_workdir):
        tmp_path, img = tmp_workdir
        r = run_tool("isolate-threshold", "isolate-threshold.sh", [img])
        assert r.returncode == 0
        out = str(tmp_path / "input-threshold.png")
        assert_valid_image(out)

    def test_explicit_options(self, run_tool, tmp_workdir):
        tmp_path, img = tmp_workdir
        out = str(tmp_path / "thresh.png")
        r = run_tool("isolate-threshold", "isolate-threshold.sh", [
            img, out, "--scale", "2", "--threshold", "40", "--color", "#00ff00",
        ])
        assert r.returncode == 0
        assert_valid_image(out)

    def test_scale_increases_dimensions(self, run_tool, tmp_workdir):
        tmp_path, img = tmp_workdir
        out = str(tmp_path / "scaled.png")
        r = run_tool("isolate-threshold", "isolate-threshold.sh", [
            img, out, "--scale", "2",
        ])
        assert r.returncode == 0
        result = assert_valid_image(out)
        # Original is 64x64, scale 2 → 128x128
        assert result.size == (128, 128)

    def test_missing_input(self, run_tool):
        r = run_tool("isolate-threshold", "isolate-threshold.sh", ["/nonexistent/image.png"])
        assert r.returncode != 0
        assert "not found" in r.stderr.lower()

    def test_no_args(self, run_tool):
        r = run_tool("isolate-threshold", "isolate-threshold.sh", [])
        assert r.returncode != 0
        assert "Usage:" in r.stderr
