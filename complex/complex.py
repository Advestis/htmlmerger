import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.graph_objs import Figure
from typing import Union, Tuple, SupportsFloat


class ForbiddenAssignmentError(Exception):
    pass


PROTECTED_ATTRIBUTES = ["_Complex__a", "_Complex__b", "_Complex__r", "_Complex__theta"]
ATTRIBUTES = ["a", "b", "r", "theta"]
CARTESIAN_ATTRIBUTES = ["a", "b"]


def compatible_numbers(n1: float, n2: float, threshold: float = 1e-8) -> bool:
    """Returns True of both numbers are equal or almost the same"""
    if n1 == n2:
        return True

    if abs((n1 - n2) / n1) < threshold:
        return True

    return False


def r_theta_from_ab(a: Union[float, None], b: [float, None]) -> [Tuple[float, float], Tuple[None, None]]:
    if a is None or b is None:
        return None, None
    r = math.sqrt(a ** 2 + b ** 2)
    if b > 0:
        theta = math.acos(a / r)
    else:
        theta = -math.acos(a / r)

    if abs(theta) < 1e-15:
        theta = 0.0
    return r, theta


def ab_from_r_theta(r: [float, None], theta: [float, None]) -> [Tuple[float, float], Tuple[None, None]]:
    if r is None or theta is None:
        return None, None
    a = r * math.cos(theta)
    b = r * math.sin(theta)
    if abs(a) < 1e-15:
        a = 0.0
    if abs(b) < 1e-15:
        b = 0.0
    return a, b


class Complex:
    def __init__(
        self,
        a: Union[float, "Complex"] = None,
        b: float = None,
        r: float = None,
        theta: float = None,
        s: str = None,
        z: "Complex" = None,
    ):
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(3, 4, 5, 0.9)
        Traceback (most recent call last):
          ...
        ValueError: You specified both cartesian and trigo representations but the values are not compatible
        >>> znumber = Complex(3, 4, 5, 0.9272952180016123)

        >>> znumber = Complex(r=5, theta=0.9272952180016123)
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="3+4i")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="3")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        0.0
        >>> print(znumber.r)
        3.0
        >>> print(znumber.theta)
        0.0

        >>> znumber = Complex(s="4i")
        >>> print(znumber.a)
        0.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        4.0
        >>> print(znumber.theta)
        1.5707963267948966

        >>> znumber = Complex(s="3cos(0)")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        0.0
        >>> print(znumber.r)
        3.0
        >>> print(znumber.theta)
        0.0

        >>> znumber = Complex(s="4isin(1.5707963267948966)")
        >>> print(znumber.a)
        0.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        4.0
        >>> print(znumber.theta)
        1.5707963267948966

        >>> # In case your string can not be a complex (here we would have two different r for instance),
        >>> # it is the part in 'cos' that is used.
        >>> znumber = Complex(s="3cos(4) + 4isin(1)")
        >>> print(znumber.a)
        -1.960930862590836
        >>> print(znumber.b)
        -2.2704074859237844
        >>> print(znumber.r)
        3.0
        >>> print(znumber.theta)
        4.0

        >>> znumber = Complex(s="3 + 4 * i")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="5e^0.9272952180016123i")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="5*(cos(0.9272952180016123i) + isin(0.9272952180016123i)")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber_2 = Complex(z=znumber)
        >>> print(znumber_2.a)
        3.0
        >>> print(znumber_2.b)
        4.0
        >>> print(znumber_2.r)
        5.0
        >>> print(znumber_2.theta)
        0.9272952180016123

        >>> znumber_2 = Complex(znumber)
        >>> print(znumber_2.a)
        3.0
        >>> print(znumber_2.b)
        4.0
        >>> print(znumber_2.r)
        5.0
        >>> print(znumber_2.theta)
        0.9272952180016123

        """

        if isinstance(a, Complex):
            z = a
            a = None
            b = None
            r = None
            theta = None

        if r is not None and r < 0:
            raise ValueError("A complex number's norm cannot be negative!")

        self.__a = float(a) if a is not None else None
        self.__b = float(b) if b is not None else None
        self.__r = float(r) if r is not None else None
        self.__theta = float(theta) if theta is not None else None

        if z:
            self.a = z.a
            self.b = z.b
            self.r = z.r
            self.theta = z.theta
        elif s:
            self._guess_repr_from_string(s)
        else:
            self._guess_repr()

    @property
    def conjugate(self, repres: str = "cartesian"):
        if repres == "cartesian":
            return Complex(self.a, -self.b)
        elif repres == "trigo" or repres == "exp":
            return Complex(r=self.r, theta=-self.theta)
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_repr()

    def to_string(self, repres: str = "cartesian") -> str:
        """ Human-readable str

        Examples
        --------
        >>> z = Complex(3, 3)
        >>> print(z)
        3.0 + 3.0i
        >>> print(z.to_string("trigo"))
        4.242640687119285 * (cos(0.7853981633974483) + isin(0.7853981633974483))
        >>> print(z.to_string("exp"))
        4.242640687119285e^0.7853981633974483i

        """
        bsign = "+" if self.b > 0 else "-"
        if repres == "cartesian":
            return f"{self.a} {bsign} {abs(self.b)}i"
        elif repres == "trigo":
            return f"{self.r} * (cos({self.theta}) + isin({self.theta}))"
        elif repres == "exp":
            return f"{self.r}e^{self.theta}i"
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def to_repr(self, repres: str = "cartesian") -> str:
        """ str readable by exec() or eval()

        Examples
        --------
        >>> z = Complex(3, 3)
        >>> print(repr(z))
        3.0 + 3.0 * i
        >>> print(z.to_repr("trigo"))
        4.242640687119285 * (cos(0.7853981633974483) + i * sin(0.7853981633974483))
        >>> print(z.to_repr("exp"))
        4.242640687119285 * e ** (0.7853981633974483 * i)

        """
        bsign = "+" if self.b > 0 else "-"
        if repres == "cartesian":
            return f"{self.a} {bsign} {abs(self.b)} * i"
        elif repres == "trigo":
            return f"{self.r} * (cos({self.theta}) + i * sin({self.theta}))"
        elif repres == "exp":
            return f"{self.r} * e ** ({self.theta} * i)"
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    # Class methods

    def to_latex(self, repres: str = "cartesian") -> str:
        """

        Examples
        --------
        >>> z = Complex(3, 3)
        >>> print(z.to_latex())
        $3.0 + 3.0i$
        >>> print(z.to_latex("trigo"))
        $4.242640687119285 \\times (\\cos(0.7853981633974483) + i \\sin(0.7853981633974483))$
        >>> print(z.to_latex("exp"))
        $4.242640687119285 \\text{e}^{0.7853981633974483 i}$

        """
        if repres == "cartesian":
            return f"${self.a} + {self.b}i$"
        elif repres == "trigo":
            return f"${self.r} \\times (\\cos({self.theta}) + i \\sin({self.theta}))$"
        elif repres == "exp":
            return f"${self.r} \\text{{e}}^{{{self.theta} i}}$"
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def round(self, n: int, repres: str = "cartesian") -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.round(n=2))
        3.12 + 4.79i
        >>> print((znumber.round(n=2, repres="exp")).to_string("exp"))
        5.72e^0.99i

        """
        if repres == "cartesian":
            return Complex(round(self.a, n), round(self.b, n))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=round(self.r, n), theta=round(self.theta, n))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def ceil(self, repres: str = "cartesian") -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.ceil())
        4.0 + 5.0i
        >>> print((znumber.ceil(repres="exp")).to_string("exp"))
        6.0e^1.0i

        """
        if repres == "cartesian":
            return Complex(math.ceil(self.a), math.ceil(self.b))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=math.ceil(self.r), theta=math.ceil(self.theta))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def floor(self, repres: str = "cartesian") -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.floor())
        3.0 + 4.0i
        >>> print((znumber.floor(repres="exp")).to_string("exp"))
        5.0e^0.0i

        """
        if repres == "cartesian":
            return Complex(math.floor(self.a), math.floor(self.b))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=math.floor(self.r), theta=math.floor(self.theta))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def trunc(self, repres: str = "cartesian") -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.trunc())
        3.0 + 4.0i
        >>> print((znumber.trunc(repres="exp")).to_string("exp"))
        5.0e^0.0i

        """
        if repres == "cartesian":
            return Complex(math.trunc(self.a), math.trunc(self.b))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=math.trunc(self.r), theta=math.trunc(self.theta))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def plot(self, fig: Figure = None, **kwargs) -> Figure:
        if fig is None:
            fig = px.scatter(
                pd.DataFrame(columns=["$\\mathbb{R}$", "$\\mathbb{C}$"], data=[[self.a, self.b]]),
                x="$\\mathbb{R}$",
                y="$\\mathbb{C}$",
                **kwargs,
            )
        else:
            fig.add_trace(go.Scatter(x=[self.a], y=[self.b], mode="markers", **kwargs))
        return fig

    @property
    def a(self):
        if str(self.__a) == "-0.0":
            return 0.0
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value
        self.__r, self.__theta = r_theta_from_ab(self.a, self.b)

    @property
    def b(self):
        if str(self.__b) == "-0.0":
            return 0.0
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = value
        self.__r, self.__theta = r_theta_from_ab(self.a, self.b)

    @property
    def r(self):
        if str(self.__r) == "-0.0":
            return 0.0
        return self.__r

    @r.setter
    def r(self, value):
        self.__r = value
        self.__a, self.__b = ab_from_r_theta(self.r, self.theta)

    @property
    def theta(self):
        if str(self.__theta) == "-0.0":
            return 0.0
        return self.__theta

    @theta.setter
    def theta(self, value):
        self.__theta = value
        self.__a, self.__b = ab_from_r_theta(self.r, self.theta)

    @property
    def mod(self) -> float:
        """

        Examples
        --------
        >>> z = Complex(3, 4)
        >>> print(z.mod)
        5.0
        >>> z = Complex(r=2, theta=5)
        >>> print(z.mod)
        2.0
        """
        return self.__abs__()

    @property
    def arg(self) -> float:
        """

        Examples
        --------
        >>> z = Complex(3, 4)
        >>> print(z.arg)
        0.9272952180016123
        >>> z = Complex(r=2, theta=5)
        >>> print(z.arg)
        5.0
        """
        return self.theta

    # Comparison

    def __eq__(self, other: Union[int, float, "Complex", str]) -> bool:
        """

        Example
        -------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(r=5, theta=0.9272952180016123)
        >>> znumber == znumber2
        True

        """
        if isinstance(other, str):
            other = Complex(s=other)
        if isinstance(other, Complex):
            if self.a == other.a and self.b == other.b:
                return True
            if self.r == other.r and self.theta == other.theta:
                return True
        elif self.a == other:
            return True
        return False

    def __ne__(self, other: Union[int, float, "Complex", str]) -> bool:
        """

        Example
        -------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(r=5, theta=0.9272952180016123)
        >>> znumber != znumber2
        False

        """
        if not self.__eq__(other):
            return True
        return False

    def __lt__(self, other) -> bool:
        raise ArithmeticError("Complex numbers can not be compared!")

    def __gt__(self, other) -> bool:
        raise ArithmeticError("Complex numbers can not be compared!")

    def __le__(self, other) -> bool:
        raise ArithmeticError("Complex numbers can not be compared!")

    def __ge__(self, other) -> bool:
        raise ArithmeticError("Complex numbers can not be compared!")

    # Unary arithmetic operators

    def __pos__(self) -> "Complex":
        return self

    def __neg__(self) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> z2 = -znumber
        >>> print(z2)
        -3.0 - 4.0i

        """
        return Complex(a=-self.a, b=-self.b)

    def __abs__(self) -> float:
        return self.r

    def __round__(self, n: int = 0) -> "Complex":
        return self.round(n=n)

    def __floor__(self) -> "Complex":
        return self.floor()

    def __ceil__(self) -> "Complex":
        return self.ceil()

    def __trunc__(self) -> "Complex":
        return self.trunc()

    # Normal arithmetic operators

    def __add__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(5, 6)
        >>> print(znumber + znumber2)
        8.0 + 10.0i
        >>> znumber2 = "5 + 6i"
        >>> print(znumber + znumber2)
        8.0 + 10.0i
        >>> znumber2 = 5
        >>> print(znumber + znumber2)
        8.0 + 4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.a = new.a + other.a
            new.b = new.b + other.b
        else:
            new.a = new.a + other
        return new

    def __sub__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(5, 6)
        >>> print(znumber - znumber2)
        -2.0 - 2.0i
        >>> znumber2 = "5 + 6i"
        >>> print(znumber - znumber2)
        -2.0 - 2.0i
        >>> znumber2 = 5
        >>> print(znumber - znumber2)
        -2.0 + 4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.a = new.a - other.a
            new.b = new.b - other.b
        else:
            new.a = new.a - other
        return new

    def __mul__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber2 = Complex(r=5, theta=6)
        >>> print((znumber * znumber2).to_string("exp"))
        15.0e^10.0i
        >>> znumber2 = "5e^6i"
        >>> print((znumber * znumber2).to_string("exp"))
        15.0e^10.0i
        >>> znumber2 = 5
        >>> print((znumber * znumber2).to_string("exp"))
        15.0e^4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.r = new.r * other.r
            new.theta = new.theta + other.theta
        else:
            new.r = new.r * other
        return new

    def __truediv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber2 = Complex(r=5, theta=6)
        >>> print((znumber / znumber2).to_string("exp"))
        0.6e^-2.0i
        >>> znumber2 = "5e^6i"
        >>> print((znumber / znumber2).to_string("exp"))
        0.6e^-2.0i
        >>> znumber2 = 5
        >>> print((znumber / znumber2).to_string("exp"))
        0.6e^4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.r = new.r / other.r
            new.theta = new.theta - other.theta
        else:
            new.r = new.r / other
        return new

    def __pow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber2 = Complex(r=5, theta=6)
        >>> print((znumber ** znumber2).to_string("exp"))
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'Complex'
        >>> znumber2 = "5e^6i"
        >>> print((znumber ** znumber2).to_string("exp"))
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'str'
        >>> znumber2 = 5
        >>> print((znumber ** znumber2).to_string("exp"))
        243.0e^20.0i

        """
        new = Complex(self)

        if isinstance(other, str) or isinstance(other, Complex):
            return NotImplemented
        new.r = new.r ** other
        new.theta = new.theta * other
        return new

    # Reflected arithmetic operators

    def __radd__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(1 + znumber)
        4.0 + 4.0i

        """
        return self + other

    def __rsub__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(1 - znumber)
        2.0 + 4.0i

        """
        return self - other

    def __rmul__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(2 * znumber)
        6.0 + 8.0i

        """
        return self * other

    def __rtruediv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(3 / znumber)
        0.36 - 0.48i

        """
        return self.conjugate * other / self.mod ** 2

    def __rpow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        return NotImplemented

    # Augmented assignment

    def __iadd__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber += Complex(5, 6)
        >>> print(znumber)
        8.0 + 10.0i

        """
        return self + other

    def __isub__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber -= Complex(5, 6)
        >>> print(znumber)
        -2.0 - 2.0i

        """
        return self - other

    def __imul__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber *= Complex(r=5, theta=6)
        >>> print(znumber.to_string("exp"))
        15.0e^10.0i

        """
        return self * other

    def __idiv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber /= Complex(r=5, theta=6)
        >>> print(znumber.to_string("exp"))
        0.6e^-2.0i

        """
        return self / other

    def __ipow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber **= Complex(r=5, theta=6)
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'Complex'
        >>> znumber **= "5e^6i"
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'str'
        >>> znumber **= 5
        >>> print(znumber.to_string("exp"))
        243.0e^20.0i

        """
        return self ** other

    def __copy__(self) -> "Complex":
        return Complex(z=self)

    def __setattr__(self, key, value):
        """

        Examples
        --------
        >>> z = Complex(3, 4)
        >>> z.r
        5.0
        >>> z.q = 2
        Traceback (most recent call last):
        ...
        complex.ForbiddenAssignmentError: The Complex class does not allow for new attributes assignment
        >>> z.a = 4
        >>> z.r
        5.656854249492381
        >>> z.__r = 4
        Traceback (most recent call last):
        ...
        complex.ForbiddenAssignmentError: The Complex class does not allow for new attributes assignment
        """
        if key not in ATTRIBUTES and key not in PROTECTED_ATTRIBUTES:
            raise ForbiddenAssignmentError("The Complex class does not allow for new attributes assignment")
        super().__setattr__(key, value)

    __deepcopy__ = __copy__

    # Internal methods

    def _guess_repr(self) -> None:
        cartesian = False
        trigo = False

        if self.__a is not None and self.__b is not None:
            cartesian = True
        if self.__r is not None and self.__theta is not None:
            trigo = True
        if not cartesian and not trigo:
            raise ValueError("Not enough information provided at Complex number creation.")

        if cartesian:
            r, theta = r_theta_from_ab(self.__a, self.__b)
            if trigo:
                # Do not set self.r and self.theta if trigo representation was found, since they were already specified
                # by the user. Just check that those values are compatible with the given a and b
                if not compatible_numbers(r, self.__r) or not compatible_numbers(theta, self.__theta):
                    raise ValueError(
                        "You specified both cartesian and trigo representations but the values are not compatible"
                    )
            else:
                self.a = self.__a
                self.b = self.__b
        # If trigo, then not cartesian too. Set a and b.
        else:
            self.r = self.__r
            self.theta = self.__theta

    def _guess_repr_from_string(self, s) -> None:
        s = s.replace("(", "")
        s = s.replace(")", "")
        s = s.replace("*", "")
        s = s.replace("x", "")
        s = s.replace(" ", "")
        # TODO Add possibility to write something like '3 x e^(i x pi / 4)'
        if "e^" in s or "exp" in s:
            s = s.replace("i", "")
            if "e^" in s:
                self.r = float(s.split("e^")[0])
                self.theta = float(s.split("e^")[1])
            else:
                self.r = float(s.split("exp")[0])
                self.theta = float(s.split("exp")[1])
        elif "cos" in s or "sin" in s:
            ss = s.split("+")[0].replace("i", "")
            if "cos" in ss:
                self.r = float(ss.split("cos")[0])
                self.theta = float(ss.split("cos")[1])
            else:
                self.r = float(ss.split("sn")[0])
                self.theta = float(ss.split("sn")[1])
        else:
            if "+" not in s:
                if "i" in s:
                    self.a = 0.0
                    self.b = float(s.replace("i", ""))
                else:
                    self.a = float(s)
                    self.b = 0.0
            else:
                self.a = float(s.split("+")[0].replace(" ", ""))
                self.b = float(s.split("+")[1].replace(" ", "").replace("i", ""))


i = Complex(0, 1)

mathexp = math.exp


def myexp(x) -> Union[float, Complex]:
    if isinstance(x, Complex):
        return mathexp(x.a) * Complex(r=1, theta=x.b)
    else:
        return mathexp(x)


math.exp = myexp

mathlog = math.log


def mylog(x: Union[SupportsFloat, Complex], base=None) -> Union[float, Complex]:
    if isinstance(x, Complex):
        if base is None:
            return mathlog(x.r) + i * x.theta
        else:
            return mathlog(x.r, base) + i * x.theta / mathlog(base)
    else:
        print(x)
        if base is None:
            return mathlog(x)
        else:
            return mathlog(x, base)


math.log = mylog
