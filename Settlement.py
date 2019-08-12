import numpy as np
from Household import Household
from Patch import Patch
class Settlement:
	#test
	#Attributes
	__settlement_id = 0
	__household_List= np.empty(250, dtype= Household) #list of household objects belonging to this settlement
	__population = 0
	__num_households = 0
	__grain = 0
	#__neighbors = [] # list of settlement objects
	__colour = "white"
	__coordinates = [] #list of x and y coordinates of the position of the settlements

	"""docstring for Settlement"""
	def __init__(self, __settlement_id, __population, __num_households, __grain, __colour):
		self.__settlement_id = __settlement_id
		self.__population = __population
		self.__num_households = __num_households
		self.__grain = __grain
		self.__colour = __colour

	def __init__(self, __settlement_id, __population, __num_households):
		self.__settlement_id = __settlement_id
		self.__population = __population
		self.__num_households = __num_households

	def getCoordinates(self):
		return self.__coordinates

	def checkSettlementPopulation(self):
		#Size 1 - small ; 2 - medium ; 3 large ; 4 XL
		#Same as setSize() method that used to be in this class
		if self.__population <= 0:
			#removeSettlement
			return 0
		elif self.__population > 150:
			return 4
		elif (self.__population > 100 and self.__population <= 150) :
			return 3
		elif (self.__population > 49 and self.__population <= 100):
			return 2
		else:
			return 1

	def addHousehold(self, household):
		pass

	def setHouseholds(self, householdList):
		#Called from setUpSettlements in simulate class - sets the households in each settlement
		#self.__settlement_id = __settlement_id
		#__settlement_id += 1
		self.__household_List = householdList
		#takes in either a list of household objects or just one household object
		#adds/removes a household for populationShift() OR fission()
		#self.__households.append(household)

	def getHouseholdList(self):
		return self.__household_List

	def setSize():
		pass

	def setCoordinates(self, coords):
		self.__coordinates = coords


	def setSize():
		#
		pass
		
	def removeHousehold(self, household):
		count = 0
		for i in self.__households:
			if self.household_size <= 0: #delete if no one lives here
				self.__households.remove(count)
			if i == household: #delete the household passed through as a parameter
				self.__households.remove(count)
			count+=1
