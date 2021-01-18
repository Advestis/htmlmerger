---
permalink: /docs/index.html
---

**The official documentation is available at https://advestis.github.io/htmlmerger/**

# HtmlMerger

A package allowing to merge all html files in a directory in a single file.

## Installation

```
git clone https://github.com/pcotteadvestis/htmlmerger
cd htmlmerger
python setup.py install
```

or

```
pip install htmlmerger
```

## Usage

Merges html files into a fingle file

For each file, will extract the content between the <html><body><head> ... <\\head><\\body><\\html> or
<html><body> ... <\\body><\\html> and put all those contents between those same tags in a new file. Simple as
that.

You can either give a list of files or a directory as input, and if not specified the output will be
input_directory/merged.html, or ./merged.html. You can also pass the argument "clean=True" when calling merge() to
delete the
individual files
used for merging.

Supports transparentpath objects.

```python
from htmlmerger import HtmlMerger
merger = HtmlMerger(input_directory="my_htmls/")  # result will be in my_htmls/merged.html
merger.merge(clean=True)  # or clean=False to keep the individual files (default behavior)

from pathlib import Path
merger = HtmlMerger(files=Path("my_htmls/").glob("*"))  # result will be in ./merged.html
merger.merge()
```