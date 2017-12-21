__author__ = "Zylanx"

"""
	New class-based implimentation of the user wallet 
	A more robust impl using classes that impliment more verification checks
	and other improvements
"""

# TODO: Btw Alex, if you are going to be using decimal, you should be keeping that consistent
# If you use decimal, then it should be stored in the db as decimal/numeric
# as that keeps it accurate and stops it losing precision.
# The point of using decimal is that it can be used fixed point.
# storing that as a float just wrecks that and makes it inaccurate,
# especially since you _always_ want to be rounding down

# TODO: Make this all compatible with asyncio

from decimal import Decimal, ROUND_DOWN

class CurrencyError(Exception): # TODO: Change to a proper d.py error and handle it
	""" A generic error raised by the currency class """
	pass

class CurrencyValidationError(CurrencyError):
	""" Error asserting that the validation check failed """
	pass

class Currency():
	""" A currency class that integrates verification as part of the class """

	# unneeded
	#__decZero = decimal.Decimal('0')
	#__decInf = decimal.Decimal('inf')

	def __init__(self, value: str, places: int = 2):
		self.places = places
		self.placesDec = Decimal('10') ** -places # Gets the exponent for .quantize. 10**-2 = 0.01. TODO: give a better name
		self.value = Decimal(value).quantize(self.placesDec, rounding = ROUND_DOWN) # Round and fit the value to a given place

		if self.isNan():
			raise CurrencyError() # TODO: Write an exception message

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return repr(self.value)

	def isPositiveOrZero(self) -> bool:
		""" True when zero (+ or -) or a finite number that is not signed """
		if (self.value.is_zero) or (self.value.is_finite() and not self.value.is_signed()):
			return True
		else:
			return False

	def isNegative(self) -> bool:
		""" True when finite and signed and not zero """
		if (not self.value.is_zero()) and (self.value.is_finite() and self.value.is_signed()):
			return True
		else:
			return False

	def isNumber(self) -> bool:
		""" True when finite and not Nan """
		if self.value.is_finite():
			return True
		else:
			return False

	def isNan(self) -> bool:
		if self.value.is_nan():
			return True
		else:
			return False

	def mult(self, multiplier: Decimal, rounding: str = ROUND_DOWN) -> Decimal:
		""" Multiply the instance by a Decimal()
			These are only provided for ease of use by getting rid of the quantize() step """
		value = self.value * multiplier
		value = value.quantize(self.placesDec, rounding = rounding)
		# TODO: insert checks
		self.value = value
		return value

	def divide(self, divisor: Decimal, rounding: str = ROUND_DOWN) -> Decimal:
		""" Divide the instance by a Decimal()
			These are only provided for ease of use by getting rid of the quantize() step """
		value = self.value / divisor
		value = value.quantize(self.placesDec, rounding = rounding)
		# TODO: insert checks
		self.value = value
		return value

	def quantize(self, rounding = ROUND_DOWN):
		""" Quantize the value back to the required currency format """
		self.value = self.value.quantize(self.placesDec, rounding = rounding)

class Wallet():
	""" A users wallet.
		provides many functions for the managment and manipulation of wallets """
	pass

if __name__ == "__main__":
	# TODO: add tests
	pass