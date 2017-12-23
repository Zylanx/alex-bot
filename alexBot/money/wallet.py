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

# TODO: Add full typecasting and checking

from decimal import Decimal, ROUND_DOWN
from .currency import Currency
from functools import wraps

class makeDirty():
	def __init__(self, func):
		self.func = func

	def __get__(self, instance, cls):
		@wraps(self.func)
		def inner(*args, **kwargs):
			retVal = self.func(instance, *args, **kwargs)
			instance.dirty = True
			return retVal
		return inner

class Wallet():
	""" A users wallet.
		provides many functions for the managment and manipulation of wallets """

	def __init__(self, manager, userID, walletBal: Decimal, decPlaces: int = 2, initRounding: str = ROUND_DOWN):
		self.userID = userID
		self._balance = Currency(walletBal, decPlaces, initRounding)
		self._decPlaces = decPlaces

		self.manager = manager
		self.dirty = False

	@property
	def balance(self):
		return self._balance

	@balance.setter
	def balance(self, newVal):
		self.setBalance(newVal)

	def __repr__(self):
		return "Wallet(None, {}, {}, {})".format(self.userID, self._balance.value, self._decPlaces)

	def __str__(self):
		return "Wallet User: {}, Balance: {}".format(self.userID, self.balance)

	def flushWallet(self):
		""" Save the wallet to whatever storage is being used """
		pass

	@makeDirty
	def setBalance(self, newVal: 'Currency'):
		self._balance.value = Currency(newVal, self._decPlaces)

	@makeDirty
	def addBalance(self, amount: 'Currency'):
		self._balance.add(amount)

	@makeDirty
	def subBalance(self, amount: 'Currency'):
		self._balance.sub(amount)

	@makeDirty
	def recieve(self, amount: 'Currency'):
		self.addBalance(amount)

	@makeDirty
	def transfer(self, targetAccount: 'Wallet', amount: 'Currency'):
		# TODO: Check transferable
		# TODO: Check have enough money
		self.subBalance(amount)
		targetAccount.recieve(amount)

if __name__ == "__main__":
	# TODO: add tests
	pass