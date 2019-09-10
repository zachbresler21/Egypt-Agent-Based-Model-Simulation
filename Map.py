import numpy as np
import random
import math
from Patch import Patch


class Map:

	'''Attributes'''
	__grid = np.empty((41,41), dtype= int) #numpy array depicting the grid (list of integers)
	__patches = np.empty((41,41), dtype = Patch) #numpy array of patch objects

	'''Docstring for Map'''
	def __init__(self):
		self.__lorenz_points = 0.0
		self.__gini_index_reserve = 0.0
		self.__avg_ambition = 0.0
		self.__avg_competency = 0.0


	'''Returns the numpy grid'''
	def getGrid(self):
		return self.__grid

	'''Creates patch objects and adds them to the numpy array of patches'''
	def createPatches(self):
		#Use multiprocessing
		count = 0
		for r in range(41):
			for c in range(41):
				self.__patches[r,c] = Patch(count, True) #this should insert a Patch object - I made every Patch a Field
				count += 1
		return self.__patches
		#populate list of patches

	'''Returns a numpy array of patches'''
	def getPatches(self):
		return self.__patches

	'''Creates the river'''
	def createRiver(self):
		#making first 2 columns river
		for r in range (len(self.__patches)):
			self.__patches[0,r].toggleRiver()
			self.__patches[1,r].toggleRiver()
			self.__grid[r,0] = 0
			self.__grid[r,1] = 0
			#changing the grid and the respective patches (toggles river boolean)

	'''Generates random coordinates'''
	def generateCoords(self):
		r = random.randint(0,40)
		c = random.randint(2,40)
		return [r,c]

	'''Checks to see if the patch is available'''
	def isPatchAvailable(self,coords):
		if self.__patches[coords[0], coords[1]].isRiver() == False and self.__patches[coords[0],coords[1]].isSettlement() == False:
			return True
		else:
			return False
		#returns true if there is no settlement or river at the coordinates

	'''Sets up the settlements'''
	def setUpSettlements(self,settlement_list):
		#takes a list of settlements as a parameter
		counter = 0
		coords_list = []

		while(counter < len(settlement_list)):
			coords = self.generateCoords()
			if self.isPatchAvailable(coords) == True:
				settlement_list[counter].setCoordinates(coords) #set coords in settlement object [r,c]
				self.__patches[coords[0],coords[1]].toggleSettlement()
				coords_list.append(coords) #2d array - each element is a new set of coords of settlements
				#change patch to a settlement in the plot (return list of coords to simulate)
				counter += 1
			else:
				coords = self.generateCoords()
		return coords_list
		#if the patch is available at the randomly generated coordinates, settlement is created, otherwise coordinates will be regenerated

	'''Abstract representation of the annual Nile flood; this method assigns a fertility value to each field based on its distance to water patches'''
	def flood(self):
		patches = self.__patches
		mu = random.randint(0,10) + 5
		sigma = random.randint(0,5) + 5
		#chooses a mean a standard dev for the fertility distribution
		alpha = 2 * math.pow(sigma,2)
		beta = 1 / (sigma * math.sqrt(2 * math.pi))
		#sets up part of the normal distribution equation

		for i in range (41):
			for j in range(41):
				fertility = 17 * (beta * (math.exp(0 - math.pow((patches[i][j].findCoordinates()[0] - mu),2)/alpha))) #determines fertility
				if(patches[i][j].isField()):
					patches[i][j].inner.setFertility(fertility) #sets the field's fertility
					num = int(10*round(fertility, 1))
					if(num<=0):
						num = 2
					self.__grid[j][i] = num
					#changes the value in the grid to represent the field's colour displayed on the plot
					patches[i][j].inner.setHarvestFalse() #after every flood, field harvest is set to false
			self.createRiver()

	'''Clears everything and starts new'''
	def clearAll(self):
		__lorenz_points = 0.0
		__gini_index_reserve = 0.0
		__avg_ambition = 0.0
		__avg_competency = 0.0
		__grid = np.empty((41,41), dtype= int)
		__patches = np.empty((41,41), dtype = object)
