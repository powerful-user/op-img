"""Tests for the `op` CLI dispatcher."""

import pytest

from conftest import assert_valid_image, skip_without_imagemagick

ALL_TOOLS = [
    "bit-crush", "channel-offset", "closest-palette", "cross-hatch",
    "dot-halftone", "fold", "isolate-threshold", "line-halftone",
    "pixel-sort", "res-crush", "scan-glitch", "stipple",
]


class TestHelp:
    def test_no_args_shows_help(self, run_op):
        r = run_op([])
        assert r.returncode == 0
        assert "Usage:" in r.stdout
        assert "Available tools:" in r.stdout

    def test_help_flag(self, run_op):
        r = run_op(["--help"])
        assert r.returncode == 0
        assert "Usage:" in r.stdout

    def test_h_flag(self, run_op):
        r = run_op(["-h"])
        assert r.returncode == 0
        assert "Usage:" in r.stdout

    def test_all_tools_listed(self, run_op):
        r = run_op([])
        for tool in ALL_TOOLS:
            assert tool in r.stdout, f"Tool '{tool}' not in help output"


class TestDispatch:
    def test_dispatch_python_tool(self, run_op, tmp_workdir):
        tmp_path, img = tmp_workdir
        out = str(tmp_path / "out.png")
        r = run_op(["scan-glitch", img, out, "--severity", "1", "--seed", "1"])
        assert r.returncode == 0
        assert_valid_image(out)

    @skip_without_imagemagick()
    def test_dispatch_shell_tool(self, run_op, tmp_workdir):
        tmp_path, img = tmp_workdir
        out = str(tmp_path / "out.png")
        r = run_op(["bit-crush", img, out, "--bits", "2"])
        assert r.returncode == 0
        assert_valid_image(out)

    def test_unknown_tool(self, run_op):
        r = run_op(["nonexistent-tool"])
        assert r.returncode != 0
        assert "unknown tool" in r.stderr.lower()
        assert "Available tools:" in r.stderr
