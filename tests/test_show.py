import pytest
from click.testing import CliRunner
from cidrtool.commands.show import show


@pytest.fixture
def runner():
    return CliRunner()


def test_no_overlap_contiguous(runner):
    result = runner.invoke(show, ["192.168.0.0/25", "192.168.0.128/25"])
    assert result.exit_code == 0
    assert "There is no overlap" in result.output
    assert "192.168.0.0" in result.output
    assert "192.168.0.255" in result.output
    assert "* Total IPs: 256" in result.output


def test_with_overlap(runner):
    result = runner.invoke(show, ["192.168.0.0/24", "192.168.0.128/25"])
    assert result.exit_code == 0
    assert "overlap with" in result.output
    assert "* Total IPs:" in result.output


def test_non_contiguous_groups(runner):
    result = runner.invoke(show, ["192.168.0.0/25", "192.168.1.0/25"])
    assert result.exit_code == 0
    assert result.output.count("Total IPs") == 1
    assert "* Total IPs: 128" in result.output or "* Total IPs: 256" in result.output


def test_verbose_output(runner):
    result = runner.invoke(show, ["-v", "10.0.0.0/25", "10.0.0.128/25"])
    assert result.exit_code == 0
    assert "Final args" in result.output


def test_stdin_input(monkeypatch, runner):
    monkeypatch.setattr(
        "cidrtool.commands.show.read_args_from_stdin", lambda: ["10.0.0.0/24"]
    )
    result = runner.invoke(show, ["-"])
    assert result.exit_code == 0
    assert "* Total IPs: 256" in result.output
