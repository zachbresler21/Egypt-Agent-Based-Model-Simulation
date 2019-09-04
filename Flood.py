from Map import Map
from Patch import Patch
import random
import math


class Flood:
	#Atributes
	map = Map()

	"""docstring for Flood"""
	def __init__(self):
		self.__fertility_colour = "White"

	def setFertility(self):
		patches = self.map.getPatches()
		mu = random.randint(0,10) + 5
		sigma = random.randint(0,5) + 5
		alpha = 2 * math.pow(sigma,2)
		beta = 1 / (sigma * math.sqrt(2 * math.pi))

		for i in range (41):
			for j in range(41):
				fertility = 17 * (beta * (math.exp(0 - math.pow((patches[i][j].findCoordinates()[0] - mu),2)/alpha)))
				if(patches[i][j].isField()):
					patches[i][j].inner.setFertility(fertility)
					patches[i][j].inner.setHarvestFalse()
		self.map.gridRecolour()
