__author__ = "Zylanx"

"""
	New class-based implimentation of the user wallet 
	A more robust impl using classes that impliment more verification checks
	and other improvements
"""

"""
	Just as a side comment. this has become slightly monolithic.
	It is also very incomplete with only just enough to get the thing working
"""

# TODO: Make this all compatible with asyncio
# TODO: Reformat code to comply with authors code style
# TODO: Impliment more checks related to the flags set by Decimal
# TODO: Add error handling to make things a bit more responsive and not crash-happy

from decimal import Decimal, ROUND_DOWN
from functools import wraps

def currencyToDec(func):
	@wraps(func)
	def inner(*args, **kwargs):
		retVal = func(*args, **kwargs)
		return retVal.value
	return inner

class CurrencyError(Exception):
	""" A generic error raised by the currency class """
	pass

class CurrencyValidationError(CurrencyError):
	""" Error asserting that the validation check failed """
	pass

# TODO: Maybe make this just extend Decimal? No, That is more anoying than it is worth
class Currency():
	""" A currency class that integrates verification as part of the class """

	def __init__(self, value: str = '0.00', places: int = 2, initRounding: str = ROUND_DOWN):
		self._places = places
		self._placesExp = Decimal('10') ** -places # Gets the exponent for .quantize. 10**-2 = 0.01
		self._value = Decimal(value)

		# TODO: Implement proper casting

		if self.isNan():
			raise CurrencyError("Value was NaN")

		self.quantize(initRounding)

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, newVal):
		if isinstance(newVal, Currency):
			# TODO: Add a log that warns this may not be implemented correctly yet
			self._value = newVal.value
		else:
			self._value = Decimal(newVal)
			self.quantize()

	@property
	def places(self):
		""" Gets the number of decimal places """
		return self._places

	@places.setter
	def places(self, places):
		""" Sets the number of decimal places and updates the internal decimal representation
			Warning: setting it to a smaller number than a larger number will cause the number to lose precision """
		self._places = places
		self._placesExp = Decimal('10') ** -places
		self.quantize()

	def quantize(self, rounding: str = ROUND_DOWN):
		""" Quantize the value back to the required currency format """
		if not self.isInf():
			self._value = self._value.quantize(self._placesExp, rounding = rounding)

	def add(self, other: 'Currency') -> Decimal:
		""" Add the instance with a Decimal() (Contained in currency)
			.quantize afterwards to make sure it is still accurate """
		if isinstance(other, Currency):
			other = other.value

		self._value = self._value + other
		return self._value

	def sub(self, other: 'Currency') -> Decimal:
		""" Add the instance with a Decimal()
			.quantize afterwards to make sure it is still accurate """
		if isinstance(other, Currency):
			other = other.value

		self._value = self._value - other
		return self._value

	def mult(self, other: 'Currency') -> Decimal:
		""" Multiply the instance by a Decimal()
			.quantize afterwards to make sure it is still accurate """
		if isinstance(other, Currency):
			multiplier = other.value

		self._value = self._value * other
		# TODO: insert checks
		return self._value

	def div(self, other: 'Currency') -> Decimal:
		""" Divide the instance by a Decimal()
			.quantize afterwards to make sure it is still accurate """
		if isinstance(other, Currency):
			divisor = other.value
		self._value = self._value / other
		# TODO: insert checks
		return self._value

	# TODO: Think about changing verification funcs to instead raise errors
	def isTransferableAmount(self) -> bool:
		""" Returns True if the value is a valid transferable amount
			finite, not nan, not negative """
		return self.isPositive() and not self.isInf()

	def isPositive(self) -> bool:
		""" True when non-NaN, not signed, and not zero"""
		return not self._value.is_zero() and not self._value.is_nan() and not self._value.is_signed()

	def isPositiveOrZero(self) -> bool:
		""" True when zero (+ or -) or a non-NaN number that is not signed """
		return self._value.is_zero() or (not self._value.is_nan() and not self._value.is_signed())

	def isNegative(self) -> bool:
		""" True when non-NaN, and signed, and not zero """
		return (not self._value.is_zero()) and (not self._value.is_nan() and self._value.is_signed())

	# Positive has one, so why not Negative too
	def isNegativeOrZero(self) -> bool:
		""" True when zero or non-NaN and signed"""
		return self._value.is_zero() or (not self._value.is_nan() and self._value.is_signed())

	def isNan(self) -> bool:
		""" True when NaN """
		return self._value.is_nan()

	def isInf(self) -> bool:
		""" True when +/-Inf """
		return self._value.is_infinite()

	def isPosInf(self) -> bool:
		""" True when Inf """
		return self.isInf() and not self._value.is_signed()

	def isNegInf(self) -> bool:
		""" True when -Inf """
		return self.isInf and self._value.is_signed()

	# Delegate Arithmetic and other ops to the value

	def __str__(self) -> str:
		return str(self._value)

	def __repr__(self) -> str:
		return "Currency({}, {})".format(repr(self._value), self._places)

	def __bool__(self) -> bool:
		return self._value.__bool__()

	def __eq__(self, other) -> bool:
		if isinstance(other, Currency):
			other = other.value
		return self._value.__eq__(other)

	def __lt__(self, other) -> bool:
		if isinstance(other, Currency):
			other = other.value
		return self._value.__lt__(other)

	def __le__(self, other) -> bool:
		if isinstance(other, Currency):
			other = other.value
		return self._value.__le__(other)

	def __gt__(self, other) -> bool:
		if isinstance(other, Currency):
			other = other.value
		return self._value.__gt__(other)

	def __ge__(self, other) -> bool:
		if isinstance(other, Currency):
			other = other.value
		return self._value.__ge__(other)

	def __neg__(self) -> 'Currency':
		return Currency(self._value.__neg__(), self.places)

	def __pos__(self) -> 'Currency':
		return Currency(self._value.__pos__(), self.places)

	def __abs__(self) -> 'Currency':
		return Currency(self._value.__abs__(), self.places)

	def __add__(self, other: 'Currency'):
		if isinstance(other, Currency):
			other = other.value
		return Currency(self._value.__add__(other), self._places)

	__radd__ = currencyToDec(__add__)

	def __sub__(self, other: 'Currency') -> 'Currency':
		if isinstance(other, Currency):
			other = other.value
		return Currency(self._value.__sub__(other))

	__rsub__ = currencyToDec(__sub__)

	def __mul__(self, other: 'Currency') -> 'Currency':
		if isinstance(other, Currency):
			other = other.value
		return Currency(self._value.__mul__(other), self._places)

	__rmul__ = currencyToDec(__mul__)

	def __truediv__(self, other: 'Currency') -> 'Currency':
		if isinstance(other, Currency):
			other = other.value
		return Currency(self._value.__truediv__(other))

	def __divmod__(self, other: 'Currency') -> 'Currency':
		if isinstance(other, Currency):
			other = other.value
		return Currency(self._value.__divmod__(other))

	def __mod__(self, other: 'Currency') -> 'Currency':
		if isinstance(other, Currency):
			other = other.value
		return Currency(self._value.__mod__(other))

	def __floordiv__(self, other: 'Currency') -> 'Currency':
		if isinstance(other, Currency):
			other = other.value
		return Currency(self._value.__floordiv__(other))

	def __float__(self):
		return self._value.__float__()

	def __int__(self):
		return self._value.__int__()

	def __trunc__(self):
		return self._value.__trunc__()

	def __round__(self, n=None) -> 'Currency':
		# Currency().quantize() preferred
		return Currency(self._value.__round__(n), n)

	def __format__(self, specifier):
		return self._value.__format__(specifier)

if __name__ == "__main__":
	# TODO: add tests
	pass