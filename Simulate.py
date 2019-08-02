class Simulate (object):
	#Attributes 
	__model_time_span = 0
	__starting_settlemenets = 0
	__starting_households = 0
	__starting_household_size = 0
	__starting_grain = 0
	__min_competency = 0.0
	__min_ambition= 0.0
	__generation_variation = 0.0
	__knowledge_radius = 0
	__distance_cost = 0
	__fallow_limit = 0
	__pop_growth_rate = 0.0
	__allow_household_fission = False
	__min_fission_chance = 0.0
	__allow_land_rental = False
	__rental_rate = 0.0
	__projected_historical_population = 0
	__household_List= [] #List of Household objects
	__settlement_List = [] #List of Settlement objects

	"""docstring for Simulate"""
	def __init__(self, arg):
		super(Simulate, self).__init__()
		self.arg = arg

	
	def clearAll():
		#clear all method

	def resetTicks():
		#resetTicks

	def setUpPatches():
		#MAP

	def setUpSettlements():
		#MAP

	def setUpHouseholds():
		#MAP

	def createRiver():
		#MAP

	def establishPopulation():
		#establishPopulation

	def populationShift():
		#popShift

	def removeHousehold():
		#rmHouse

	def fission():
		#fission

	def recolourHouseholds():
		#recolor

	def updatePlotValues():
		#need clarification on this method

	def calcTotalAmbition():
		#abmition

	def calcTotalCompetency():
		#competency

	def calcTotalPopulation():
		#totPOP
















