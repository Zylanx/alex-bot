__author__ = "Zylanx"

"""
	New class-based implimentation of the user wallet 
	A more robust impl using classes that impliment more verification checks
	and other improvements
"""

# TODO: Make this all compatible with asyncio
# TODO: Reformat code to comply with authors code style
# TODO: Impliment more checks related to the flags set by Decimal
# TODO: Add error handling to make things a bit more responsive and not crash-happy

from decimal import Decimal, ROUND_DOWN

class CurrencyError(Exception): # TODO: Change to a proper d.py error and handle it
	""" A generic error raised by the currency class """
	pass

class CurrencyValidationError(CurrencyError):
	""" Error asserting that the validation check failed """
	pass

# TODO: Maybe make this just extend Decimal?
class Currency():
	""" A currency class that integrates verification as part of the class """

	# unneeded
	#__decZero = decimal.Decimal('0')
	#__decInf = decimal.Decimal('inf')

	def __init__(self, value: str, places: int = 2):
		self.places = places
		self.placesDec = Decimal('10') ** -places # Gets the exponent for .quantize. 10**-2 = 0.01. TODO: give a better name
		# HACK: Might be better just to have a seperate one for infinite vals
		try:
			self.value = Decimal(value).quantize(self.placesDec, rounding = ROUND_DOWN) # Round and fit the value to a given place
		except:
			# Well shoot. That's no good!
			# If it is inf, just assign without quantizing
			if Decimal(value).is_infinite():
				self.value = Decimal(value)
			elif Decimal(value).is_nan():
				raise CurrencyError() # TODO: Write message, use better error

		if self.isNan():
			raise CurrencyError() # TODO: Write an exception message

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return repr(self.value)

	def setPlaces(self, places):
		""" Change the configured places
			requantizing the value is up to you to call """
		self.places = places
		self.placesDec = Decimal('10') ** -places

	# TODO: Think about changing verification funcs to instead raise errors
	def isPositive(self) -> bool:
		""" True when non-NaN, not signed, and not zero"""
		return not self.value.is_zero() and not self.value.is_nan() and not self.value.is_signed()

	def isPositiveOrZero(self) -> bool:
		""" True when zero (+ or -) or a non-NaN number that is not signed """
		return self.value.is_zero() or (not self.value.is_nan() and not self.value.is_signed())

	def isNegative(self) -> bool:
		""" True when non-NaN, and signed, and not zero """
		return (not self.value.is_zero()) and (not self.value.is_nan() and self.value.is_signed())

	# Positive has one, so why not Negative too
	def isNegativeOrZero(self) -> bool:
		""" True when zero or non-NaN and signed"""
		return self.value.is_zero() or (not self.value.is_nan() and self.value.is_signed())

	def isNan(self) -> bool:
		""" True when NaN """
		return self.value.is_nan()

	def isPosInf(self) -> bool:
		""" True when Inf """
		return self.value.is_infinite() and not self.value.is_signed()

	def isNegInf(self) -> bool:
		""" True when -Inf """
		return self.value.is_infinite() and self.value.is_signed()

	def isTransferableAmount(self) -> bool:
		""" Returns True if the value is a valid transferable amount
			finite, not nan, not negative """
		return self.isPositive() and not self.value.is_infinite()

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

	def quantize(self, rounding: str = ROUND_DOWN):
		""" Quantize the value back to the required currency format """
		self.value = self.value.quantize(self.placesDec, rounding = rounding)

if __name__ == "__main__":
	# TODO: add tests
	pass