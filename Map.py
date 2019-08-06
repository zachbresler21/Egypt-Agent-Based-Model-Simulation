import numpy as np

class Map:
	#Attributes
	__lorenz_points = 0.0
	__gini_index_reserve = 0.0
	__avg_ambition = 0.0
	__avg_competency = 0.0
	__grid = np.empty((40,40), dtype= int) #list of patches

	def __init__(self):
		self.__grid = np.random.randint(10, size= (40,40))
		
	def createRiver():
	

	def setUpSettlements(settlement_list):
		#takes a list of settlements as a parameter

	def assignFertilityColour(fertility):
		#takes a string as a parameter

	def claimField(household):
		#takes a Household object as a parameter

	def harvest():
		#harvest

	def rentField():
		#rent

	def removeLink():
		#remove

	def enlargeSettlement(factor):
		#takes an int as a parameter

	def reduceSettlement(factor):
		##takes an int as a parameter

	def recolourHouseholds():
		#recolour

	def updatePlotValues(totHouseholds, totPopulation, ambition, competency):
		#update - REVISE THE METHOD THAT IS IN THE SIMULATE CLASS

	def clearAll(self):
		#clear everything and start new 
