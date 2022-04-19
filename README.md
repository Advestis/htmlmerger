[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/htmlmerger)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
[![pytests](https://github.com/Advestis/htmlmerger/actions/workflows/pull-request.yml/badge.svg)](https://github.com/Advestis/htmlmerger/actions/workflows/pull-request.yml)
[![push-pypi](https://github.com/Advestis/htmlmerger/actions/workflows/push-pypi.yml/badge.svg)](https://github.com/Advestis/htmlmerger/actions/workflows/push-pypi.yml)
[![push-doc](https://github.com/Advestis/htmlmerger/actions/workflows/push-doc.yml/badge.svg)](https://github.com/Advestis/htmlmerger/actions/workflows/push-doc.yml)

![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![issues](https://img.shields.io/github/issues/Advestis/htmlmerger.svg)
![pr](https://img.shields.io/github/issues-pr/Advestis/htmlmerger.svg)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/htmlmerger)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:pythondev@advestis.com)

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
