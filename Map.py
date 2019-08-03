import numpy as np

class Map (object):
	#Attributes
	__lorenz_points = 0.0
	__gini_index_reserve = 0.0
	__avg_ambition = 0.0
	__avg_competency = 0.0
	__grid = np.empty((40,40),dtype = object) #numpy array

	def __init__ (self):
		count = 1
		for x in range:
			for y in range:
				self.__grid[x,y] = Patch(count, True) #this should insert a Patch object - i made every Patch a Field
				count += 1

	'''def createRiver():
		

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

 
'''









 







