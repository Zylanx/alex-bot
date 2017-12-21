__author__ = "Zylanx"

"""
	New class-based implimentation of the user wallet 
	A more robust impl using classes that impliment more verification checks
	and other improvements
"""

import decimal

class CurrencyError(Exception): # TODO: Change to a proper d.py error and handle it
	""" A generic error raised by the currency class """
	pass

class CurrencyValidationError(Exception):
	""" Error asserting that the validation check failed """
	pass

class Currency():
	""" A currency class that integrates verification as part of the class """

	# unneeded
	#__decZero = decimal.Decimal('0')
	#__decInf = decimal.Decimal('inf')

	def __init__(self, value: str, places: int = 2):
		self.places = places
		self.placesDec = decimal.Decimal('10') ** -places # Gets the exponent for .quantize. 10**-2 = 0.01. TODO: give a better name
		self.value = decimal.Decimal(value).quantize(self.placesDec, rounding = decimal.ROUND_DOWN) # Round and fit the value to a given place

		if self.value.is_nan():
			raise CurrencyError() # TODO: Write an exception message

	def isPositive(self) -> bool:
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

	def quantize(self, rounding = decimal.ROUND_DOWN):
		""" Quantize the value back to the required currency format """
		self.value = self.value.quantize(self.placesDec, rounding = rounding)

class Wallet():
	""" A users wallet.
		provides many functions for the managment and manipulation of wallets """
	pass

if __name__ == "__main__":
	# TODO: add tests
	pass