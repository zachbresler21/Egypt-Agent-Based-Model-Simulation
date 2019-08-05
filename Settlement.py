class Settlement(object):
	#test
	#Attributes
	__settlement_id = 0
	__households = [] #list of household objects belonging to this settlement
	__population = 0
	__num_households = 0
	__grain = 0
	__neighbors = [] # list of settlement objects
	__colour = "white"
	__coordinates = [] #list of x and y coordinates of the position of the settlements

	"""docstring for Settlement"""
	def __init__(self, arg):
		super(Settlement, self).__init__()
		self.arg = arg

	def checkSettlementPopulation(self):
		#Size 1 - small ; 2 - medium ; 3 large ; 4 XL
		if __population <= 0:
    			#removeSettlement
    			return 0
    		else if __population > 150:
    			return 4
    		else if (__population > 100 and __population <= 150) :
    			return 3
		else if (__population > 49 and __population <= 100):
			return 2
		else:
			return 1

	def addHousehold(self, household):
		#takes in either a list of household objects or just one household object
		
		#adds/removes a household for populationShift() OR fission()

	def removeHousehold(self, household):
		for i in __households:
			if household_size <= 0: #delete if no one lives here
				del i
			if i == household: #delete the household passed through as a parameter
				del i

