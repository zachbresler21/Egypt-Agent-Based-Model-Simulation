class Simulate:
	#Attributes
	__model_time_span = 0
	__starting_settlements = 0
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
	__household_List= [] #List of all Household objects
	__settlement_List = [] #List of all Settlement objects
	map = Map()

	def clearAll():
		#clear all method
		__settlement_List.clear()
		__household_List.clear()
		#map.clear

	def resetTicks():
		#resetTicks


	def setUpPatches():
		#MAP


	def setUpSettlements():
		#MAP
		for i in __starting_settlements:
			s = Settlement()
			__settlement_List.append(s)
			s.setHouseholds(setUpHouseholds()) #calls method in settlement class (setHouseholds) to set households in the settlements
		map.setUpSettlements(__settlement_List) #Sends to map class where it changes patches to settlements and plots settlements in grid

	def setUpHouseholds():
		#MAP
		#returns a list of households per settlement to be used in setUpSettlements
		households_for_settlement = [] #List of households to be added to settlements
		for i in startingHouseholds:
			Household h = new Household()
			households_for_settlement.append(h)
			__household_List.append(h)

		return households_for_settlement

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


	def main(self):
		#Main METHOD
		print("Simulation running")
		#Will get input from sliders later on
		__starting_settlements = int(input("Enter starting settlements: "))
		__starting_households = int(input("Enter starting households: "))
		__starting_grain = int(input("Enter starting grain: "))

		setUpSettlements()
		map.setUpSettlements(__settlement_List)



	if __name__ == "__main__":
		main()
