---
permalink: /docs/index.html
---

**The official documentation is available at https://advestis.github.io/complex/**

# Complex

A class implementing the notion of complex number

## Installation

```
git clone https://github.com/pcotteadvestis/Complex
cd Complex
python setup.py install
```

## Usage

```python
from complex import Complex
znumber = Complex(3, 4)
znumber_fromstring = Complex(s="3+4i")
znumber_fromstring_cos = Complex(s="3cos(4) + 4isin(1)")
znumber_fromstring_exp = Complex(s="5e^3.1415926i")
znumber + znumber_fromstring
z_conj = znumber.conjugate
```