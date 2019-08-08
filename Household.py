class Household (object):

	#Attributes
	__id = 0
	__size = 0
	__tot_grain = 0
	__ambtion = 0.0
	__competency = 0.0
	__knowledge_radius = 0
	__colour = ""
	__generationCountdown = 0
	__distance_cost = 0
	__allow_land_rental = False
	__rental_rate = 0.0
	__fields_owned = [] #list of Field objects
	__fields_harvested = [] #list of Field objects

	"""docstring for Household"""
	def __init__(self, __id, size ,__tot_grain, __houseColour, __fields_owned, __fields_harvested):
		super().__init__(__settlement_id, __coordinates)
		self.__id = Household.__id
		Household__id += 1
		self.__size = __size
		self.__tot_grain = __tot_grain
		self.__ambtion = 0
		self.__competency = 0
		self.__knowledge_radius = 0
		self.__houseColour = __houseColour
		self.__generationCountdown = 0
		self.__distance_cost = 0
		self.__allow_land_rental = False
		self.__rental_rate = 0
		self.__fields_owned = __fields_owned
		self.__fields_harvested = __fields_harvested

	def set_ambtion(self, __ambtion):
		self.__ambtion = __ambtion

	def set_competency(self, __competency):
		self.__competency = __competency

	def set_knowledge_radius(self, __knowledge_radius):
		self.__knowledge_radius = __knowledge_radius

	def set_generationCountdown(self, __generationCountdown):
		self.__generationCountdown = __generationCountdown

	def set_distance_cost(self, __distance_cost):
		self.__distance_cost = __distance_cost

	def set_allow_land_rental(self, __allow_land_rental):
		self.__allow_land_rental = __allow_land_rental

	def set_rental_rate(self, __rental_rate):
		self.__rental_rate = __rental_rate
		
	def claimFields():
		#

	def completeClaim():
		#

	def rentLand():
		#

	def consumeGrain():
		self.__tot_grain = self.__tot_grain - (self.__size*160)
		self.__grain = self.__grain - (self.__size*160)
		if self.__tot_grain<=0:
			self.__tot_grain = 0
			self.__size = self.__size -1

	def storageLoss():
		self.__tot_grain = self.__tot_grain - (self.__tot_grain*0.1)

	def populationShift():
		#

	def removeMember():
		s = Settlement()
		self.size = self.size - 1
		if self.size = 0:
			s.removeHousehold()

	def addMember():
		self.size = self.size + 1

	def beginFarm():
		#

	def generationalChangeover():
		#

	def removeFields():
		#

	class Farm (object):
		"""docstring for ClassName"""
		def __init__(self, arg):
			super(ClassName, self).__init__()
			self.arg = arg

		def determineField(field):
			#takes a Field object as a parameter

		def calcYield(field):
			#takes a Field object as a parameter

		def completeFarm():
			#WHAT DOES THIS DO
