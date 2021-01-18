from complex import Complex, i
import math
import pytest


# noinspection PyUnusedLocal
@pytest.mark.parametrize(
    "a, b, expected_r, expected_theta",
    [
        (3, 4, 5.0, 0.927295),
        (4, 5, 6.403124, 0.896055)
    ]
)
def test_init(fix1, a, b, expected_r, expected_theta):
    print("\n\n\nTesting init...\n")
    znumber = Complex(a, b)
    assert znumber.a == a
    assert znumber.b == b
    assert round(znumber.r, 6) == expected_r
    assert round(znumber.theta, 6) == expected_theta


# noinspection PyUnusedLocal
@pytest.mark.parametrize(
    "r, theta, expected_a, expected_b",
    [
        (5, 0.927295218, 3.0, 4.0),
        (-1, -1, None, None)
    ]
)
def test_init_r(fix1, r, theta, expected_a, expected_b):
    print("\n\n\nTesting init...\n")
    if r < 0:
        with pytest.raises(ValueError):
            Complex(r=r, theta=theta)
    else:
        znumber = Complex(r=r, theta=theta)
        assert round(znumber.a, 6) == expected_a
        assert round(znumber.b, 6) == expected_b


# noinspection PyUnusedLocal
def test_i(fix1):
    print("\n\n\nTesting i...\n")
    z = 3 + 2 * i
    assert z == Complex(3, 2)


# noinspection PyUnusedLocal
def test_expi(fix1):
    print("\n\n\nTesting expi...\n")
    z = 3 * math.exp(2 * i)
    assert z == Complex(r=3, theta=2)


# noinspection PyUnusedLocal
def test_logi(fix1):
    print("\n\n\nTesting logi...\n")
    z = Complex(r=3, theta=2)
    # noinspection PyTypeChecker
    assert math.log(z) == Complex(a=math.log(3), b=2)
