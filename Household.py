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
	def __init__(self, arg):
		super(Household, self).__init__()
		self.arg = arg
		
	def claimFields():
		#

	def completeClaim():
		#

	def rentLand():
		#

	def consumeGrain():
		#

	def storageLoss():
		#

	def populationShift():
		#

	def removeMember():
		#

	def addMember():
		#

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





			