from htmlmerger import HtmlMerger
from pathlib import Path
import pytest


expected = Path("tests/data/expected.html")


# noinspection PyUnusedLocal
@pytest.mark.parametrize(
    "files, direc, output",
    [
        (None, Path("tests/data/input"), Path("tests/data/merged.html")),
        (["tests/data/input/f1.html", "tests/data/input/f2.html"], None, Path("tests/data/merged.html"))
    ]
)
def test_init(fix1, files, direc, output):
    merger = HtmlMerger(files, direc, output)
    merger.merge()
    assert output.is_file()
    assert output.read_text() == expected.read_text()
