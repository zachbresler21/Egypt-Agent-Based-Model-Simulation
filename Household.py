#from Map import Map

class Household:

	#Attributes
	__id = 0
	__size = 0
	__tot_grain = 0
	__ambition = 0.0
	__competency = 0.0
	__knowledge_radius = 0
	__colour = ""
	__generationCountdown = 0
	__distance_cost = 0
	__allow_land_rental = False
	__rental_rate = 0.0
	__fields_owned = [] #list of Field objects
	__fields_harvested = [] #list of Field objects
	#__belongingSettlement = Settlement()

	"""docstring for Household"""
	def __init__(self,h_id, settle,size ,tot_grain, houseColour, fields_owned, fields_harvested):

		self.__id = h_id
		self.__belongingSettlement = settle
		self.__size = size
		self.__tot_grain = tot_grain
		self.__ambtion = 0
		self.__competency = 0
		self.__knowledge_radius = 0
		self.__houseColour = houseColour
		self.__generationCountdown = 0
		self.__distance_cost = 0
		self.__allow_land_rental = False
		self.__rental_rate = 0
		self.__fields_owned = fields_owned
		self.__fields_harvested = fields_harvested

	def __init__(self,h_id, settle,size, competency, ambition):
		self.__id = h_id
		self.__belongingSettlement = settle
		self.__size = size
		self.__ambtion = ambition
		self.__competency = competency

	def set_ambtion(self, ambtion):
		pass

	def set_competency(self, competency):
		self.__competency = competency

	def set_knowledge_radius(self, knowledge_radius):
		self.__knowledge_radius = knowledge_radius

	def set_generationCountdown(self, generationCountdown):
		self.__generationCountdown = generationCountdown

	def set_distance_cost(self, distance_cost):
		self.__distance_cost = distance_cost

	def set_allow_land_rental(self, allow_land_rental):
		self.__allow_land_rental = allow_land_rental

	def set_rental_rate(self, rental_rate):
		self.__rental_rate = rental_rate
		
	def claimFields():
		#
		pass

	def completeClaim():
		#
		pass

	def rentLand():
		#
		pass

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
		pass

	def removeMember():
		self.__size = self.__size - 1
		if self.__size == 0:
			self.__belongingSettlement.removeHousehold()

	def addMember():
		self.__size = self.__size + 1

	def beginFarm():
		#
		pass

	def generationalChangeover():
		#
		pass

	def removeFields():
		#
		pass

	class Farm (object):
		"""docstring for ClassName"""
		#def __init__(self, arg):
			#super(ClassName, self).__init__()
			#self.arg = arg

		def determineField(field):
			#takes a Field object as a parameter
			pass

		def calcYield(field):
			#takes a Field object as a parameter
			pass

		def completeFarm():
			#WHAT DOES THIS DO
			pass
