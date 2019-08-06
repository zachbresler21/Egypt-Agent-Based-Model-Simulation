class Settlement:
	#test
	#Attributes
	__settlement_id = 0
	__households = ["hdfg","sff","syet"] #list of household objects belonging to this settlement
	__population = 30
	__num_households = 3
	__grain = 4000
	__neighbors = [] # list of settlement objects
	__colour = "white"
	__coordinates = [] #list of x and y coordinates of the position of the settlements

	"""docstring for Settlement"""
	def __init__(self, __settlement_id, __households, __population, __num_households, __grain, __neighbors, __colour, __coordinates):
		#super(Settlement, self).__init__()
		self.__settlement_id = __settlement_id
		self.__households = __households
		self.__population = __population
		self.__num_households = __num_households
		self.__grain = __grain
		self.__neighbors = __neighbors
		self.__colour = __colour
		self.__coordinates = __coordinates

	def checkSettlementPopulation(self):
		#Size 1 - small ; 2 - medium ; 3 large ; 4 XL
		#Same as setSize() method that used to be in this class
		s = Settlement(self)
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

		#takes in either a list of household objects or just one household object
		#adds/removes a household for populationShift() OR fission()
		self.__households.append(household)


	def removeHousehold(self, household):
		count = 0
		for i in self.__households:
			if self.household_size <= 0: #delete if no one lives here
				self.__households.remove(count)
			if i == household: #delete the household passed through as a parameter
				self.__households.remove(count)
			count+=1
