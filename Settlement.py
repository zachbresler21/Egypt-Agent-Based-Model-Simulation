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

	def setHouseholds(self, householdList):
		#Called from setUpSettlements in simulate class - sets the households in each settlement
		self.__settlement_id = __settlement_id
		__settlement_id += 1
		self.__households = householdList


	def checkSettlementPopulation():
		#

	def addHousehold(household):
		#takes in either a list of household objects or just one household object

	def removeHousehold(household):
		#

	def setSize():
		#
