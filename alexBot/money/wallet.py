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

from .currency import Currency

class Wallet():
	""" A users wallet.
		provides many functions for the managment and manipulation of wallets """
	pass

if __name__ == "__main__":
	# TODO: add tests
	pass