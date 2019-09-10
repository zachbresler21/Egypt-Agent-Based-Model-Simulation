import numpy as np
from Household import Household
from Patch import Patch

class Settlement:

	'''Constructor for settlement'''
	def __init__(self, __settlement_id, __population, __num_households):
		self.__settlement_id = __settlement_id
		self.__population = __population
		self.__num_households = __num_households
		self.__coordinates = [] #row and column coordinates of the settlement
		self.__household_List= np.empty(250, dtype= Household) #list of household objects belonging to this settlement


	'''Returns the coordinates of the settlements'''
	def getCoordinates(self):
		return self.__coordinates

	'''Determines the size of the settlement with respect to its population '''
	def checkSettlementPopulation(self):
		#Size 1 - small ; 2 - medium ; 3 large ; 4 XL
		if self.__population <= 0:
			return 0
		elif self.__population > 150:
			return 24
		elif (self.__population > 100 and self.__population <= 150):
			return 20
		elif (self.__population > 49 and self.__population <= 100):
			return 17
		else:
			return 14
		#returns the size according to the population range of the settlement

	'''Sets a list of households belonging to this settlement'''
	def setHouseholds(self, householdList):
		#Called from setUpSettlements in simulate class - sets the households in each settlement
		self.__household_List = householdList
		#takes in either a list of household objects

	'''Returns a list of households belonging to this settlement'''
	def getHouseholdList(self):
		return self.__household_List

	'''Sets the coordinates of the settlement'''
	def setCoordinates(self, coords):
		self.__coordinates = coords

	'''Removes a household from household list'''
	def removeHousehold(self, household):
		self.__household_List = self.__household_List[self.__household_List != household]
		#Household object to be deleted is passed through to this method when called

	'''Increases the population of the settlement by one'''
	def incrementPopulation(self):
		self.__population += 1

	'''Decreases the population of the settlement by one'''
	def decrementPopulation(self):
		self.__population -= 1
