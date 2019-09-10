from Patch import Patch
from Map import Map
import random
import numpy as np
import math


class Household:

	'''Class variables'''
	__knowledge_radius = 0
	__distance_cost = 0
	__rental_rate = 0


	map = Map()


	"""Constructor for Household"""
	def __init__(self, h_id, size,tot_grain, competency, ambition, rental_rate, allow_land_rental, distance_cost, knowledge_radius):

		self.__id = h_id
		self.__size = size
		self.__tot_grain = tot_grain
		self.__generationCountdown = random.randint(0,5)+10
		self.__distance_cost = distance_cost
		self.__allow_land_rental = allow_land_rental
		self.__rental_rate = rental_rate
		self.__knowledge_radius = knowledge_radius
		self.__fields_owned = [] #list of the fields owned by household (list of Patch objects)
		self.__coordinates = [] #row and column coordinates of the household in the grid

		self.__competency =  competency + (random.random()*(1-competency)) #generates competency based on inputted min competency
		self.__ambition = ambition + (random.random()*(1-ambition)) #generates ambition based on inputted min competency

		self.inner = self.Farm(self) #creates an instance of Farm which is associated with Household


	'''Returns list of fields owned'''
	def getFieldsOwned(self):
		return self.__fields_owned

	'''Returns the number of workers in the household'''
	def getSize(self):
		return self.__size

	'''Returns competency of the household'''
	def getCompetency(self):
		return self.__competency

	'''Returns ambition of the household'''
	def getAmbition(self):
		return self.__ambition

	'''Returns the coordinates of the household'''
	def getCoordinates(self):
		return self.__coordinates

	'''Returns the total grain of the household'''
	def getTotGrain(self):
		return self.__tot_grain

	'''Returns the distance cost'''
	def getDistanceCost(self):
		return self.__distance_cost

	'''Adds a value to total grain'''
	def addTotGrain(self,tot_harvest):
		self.__tot_grain += tot_harvest
		#the value represents the harvest which gets passed as a paramater

	'''Removes the respective field from fields owned list'''
	def removeField(self,field):
		self.__fields_owned.remove(field)

	'''Sets the coordinates of the household'''
	def setCoordinates(self,coords):
		self.__coordinates = coords
		#called from the start of the simulation (comes from the belonging settlement coordinates)

	'''Sets the competency of the household'''
	def set_competency(self, competency):
		self.__competency = competency

	'''Sets the knowledge radius of the household'''
	def set_knowledge_radius(self, knowledge_radius):
		self.__knowledge_radius = knowledge_radius

	''''Sets the generational countdown of the household'''
	def set_generationCountdown(self, generationCountdown):
		self.__generationCountdown = generationCountdown

	'''Sets the distance cost of the household'''
	def set_distance_cost(self, distance_cost):
		self.__distance_cost = distance_cost

	'''Sets whether land rental is allowed'''
	def set_allow_land_rental(self, allow_land_rental):
		self.__allow_land_rental = allow_land_rental

	'''Sets the rental rate of the household'''
	def set_rental_rate(self, rental_rate):
		self.__rental_rate = rental_rate

	'''Returns the ID of the household'''
	def getID(self):
		return self.__id

	'''This method allows households to *decide* whether or not to claim fields that fall within their knowledge-radii.'''
	def claimFields(self, row, col):
		patches = self.map.getPatches()
		claim_chance = random.uniform(0,1) #creates a random float between 0 and 1
		if (claim_chance < self.__ambition and self.__size > len(self.__fields_owned) or len(self.__fields_owned) <= 1): #checks if household will be trying to claim land
			#The decision to claim is a function of the productivity of the field compared to existing fields and ambition.
			current_grain = self.__tot_grain
			claim_field = Patch(34567, True)
			best_fertility = 0

			r = np.arange(0, 41)
			c = np.arange(0, 41)

			cr = row
			cc = col
			#current row and column coordinates of the household
			radius = self.__knowledge_radius

			#determines indices in the circle with knowledge radius
			mask = (r[np.newaxis,:]-cr)**2 + (c[:,np.newaxis]-cc)**2 < radius**2

			for patch in patches[mask]: #traverses through array of patches in the circle
				if patch.isField() == True and patch.isOwned() == False and patch.isRiver() == False and patch.isSettlement() == False: #checks to see if the field meets criteria to be claimed
					fertility = patch.inner.getFertility()
					if fertility > best_fertility: #finds field with best fertility
						best_fertility = fertility
						claim_field = patch

			x = self.completeClaim(claim_field) #complete claim method is called
			return x #returns coordinates of the field to be claimed

	'''Completes the claim of the respective field'''
	def completeClaim(self, claim_field):
		claim_field.toggleOwned() #changes field to owned
		self.__fields_owned.append(claim_field) #adds field to list of fields owned
		return claim_field.findCoordinates()

	'''Household workers consume a certain amount of grain per year'''
	def consumeGrain(self):
		#ethnographic data suggests an adult needs an average of 160kg of grain per year to sustain.
		self.__tot_grain = self.__tot_grain - (self.__size*160) #workers consuming 160kg of grain a year
		if self.__tot_grain <= 0: #if not enough grain to feed workers, one dies
			self.__tot_grain = 0
			self.__size = self.__size - 1
			return True
		return False

	'''Checks if the househod has no more workers left'''
	def checkWorkers(self):
		if(self.__size <= 0): #if no workers left: change households field to unowned and remove household from settlement
			for field in self.__fields_owned:
				field.toggleOwned
			return True
		return False

	'''Accounts for typical annual storage loss of agricultural product'''
	def storageLoss(self):
		self.__tot_grain = self.__tot_grain - (self.__tot_grain*0.1) #reduces total grain

	'''Adds a worker to the household'''
	def addMember(self):
		self.__size = self.__size + 1 #increases the size

	'''This allows for the change of ambition and competency characteristics of a household
	   It is designed to simulate what might happen when a son/wife/daughter/nephew/brother/etc. takes over as head of household, and the resulting personality change'''
	def generationalChangeover(self,generational_variation, min_ambition, min_competency):
		self.__generationCountdown = self.__generationCountdown - 1
		if(self.__generationCountdown <= 0):
			self.__generationCountdown = random.randint(0,5) + 10
			ambition_change = random.uniform(0,generational_variation)
			decrease_chance = random.uniform(0,1)

			if(decrease_chance < 0.5):
				ambition_change = ambition_change * -1

			new_ambition = self.__ambition + ambition_change

			while(new_ambition > 1 or new_ambition < min_ambition):
				ambition_change = random.uniform(0,generational_variation)
				decrease_chance = random.uniform (0,1)
				if(decrease_chance < 0.5):
					ambition_change = ambition_change * -1

				new_ambition = self.__ambition + ambition_change
			self.__ambition = new_ambition
			#increases or decreases the ambition of the household according to arbritrary variables

			competency_change = random.uniform(0,generational_variation)
			decrease_chance = random.uniform(0,1)
			if(decrease_chance < 0.5):
				competency_change = competency_change * -1

			new_competency = self.__competency + competency_change

			while(new_competency > 1 or new_competency < min_competency):
				competency_change = random.uniform(0,generational_variation)
				decrease_chance = random.uniform (0,1)
				if(decrease_chance < 0.5):
					competency_change = competency_change * -1

				new_competency = self.__competency + competency_change

			self.__competency = new_competency
			#increases or decreases the competency of the household according to arbritrary variables

	'''If global-variable 'rent-land' is on, allows ambitious households to farm additional plots they don't own, after they and everyone else has finished their main farming/harvesting.'''
	def rentLand(self):
		patches = self.map.getPatches() #gets list of patch objects

		r = np.arange(0, 41)
		c = np.arange(0, 41)

		cr = self.__coordinates[0]
		cc = self.__coordinates[1]
		radius = self.__knowledge_radius

		mask = (r[np.newaxis,:]-cr)**2 + (c[:,np.newaxis]-cc)**2 < radius**2 #determines indices in the circle with knowledge radius

		best_harvest = 0
		total_harvest = 0
		best_field = Patch(34567, True)

		for patch in patches[mask]: #traverses through array of patches in the knowledge radius
			this_harvest = (patch.inner.getFertility()*2475*self.__competency)-(self.inner.findDistance(patch)*self.__distance_cost)
			if(patch.isField() and patch.inner.isHarvested() == False and this_harvest >= best_harvest):
				self.__best_harvest = this_harvest
				best_field = patch
		#determines the yield of the field and finds the highest yield of all unharvested fields in the knowledge radius

		harvest_chance = random.uniform(0,1)
		if(harvest_chance < self.__ambition * self.__competency):
			best_field.inner.toggleHarvested()
			total_harvest += ((best_harvest * (1 - (self.__rental_rate / 100))) - 300)
		#if high enough ambition and competency, total harvest is calculated according to the amount of yield of the best field and the rental rate

		self.__tot_grain += total_harvest
		self.inner.clearWorkersWorked()


	class Farm:

		'''Inner class of Household'''

		'''Attributes'''
		__max_potential_yield = 2475

		''''Docstring for Farm'''
		def __init__(self, household):
			self.__best_harvest = 0
			self.__workers_worked = 0
			self.__household = household

		'''Returns the amount of workers worked in the harvesting of fields for the year'''
		def getWorkersWorked(self):
			return self.__workers_worked

		'''Sets the amount of workers worked to zero'''
		def clearWorkersWorked(self):
			self.__workers_worked = 0

		'''Initiates the farming of fields and returns the coordinates of the field with the highest yield'''
		def beginFarm(self):
			best_field = self.determineField()
			if(best_field.getID() != 0):
				total_harvest = self.calcYield(best_field)
				self.__household.addTotGrain(total_harvest)
				return best_field.findCoordinates()

		'''Determines the field with the highest yield'''
		def determineField(self):
			self.__best_harvest = -100
			best_field = Patch(0, True)
			for field in self.__household.getFieldsOwned(): #traverses through fields_owned by the associated household
				this_harvest = (field.inner.getFertility()*self.__max_potential_yield*self.__household.getCompetency())-(self.findDistance(field)*self.__household.getDistanceCost())
				#yield is dependent on fertility, whether or not the household actually farms the field (competency), distance from the field and the distance cost
				if(field.inner.isHarvested() == False and this_harvest >= self.__best_harvest): #finds the highest yield field
					self.__best_harvest = this_harvest
					best_field = field
			return best_field
			#returns the field with the highest yield (the field to be harvested)

		'''Calculates the yield of the respective field'''
		def calcYield(self,field):
			#takes a Field object as a parameter
			total_harvest = 500
			farm_chance = random.uniform(0,1) #creates a random float between 0 and 1
			if(self.__household.getTotGrain() < (self.__household.getSize() * 160) or farm_chance < (self.__household.getAmbition() * self.__household.getCompetency())):
				#160 is kilograms of grain per person annually, after Hassan 1984, 63.
				field.inner.toggleHarvested()
				if(self.__best_harvest > 300):
					total_harvest = self.__best_harvest - 300  #300 = cost of seeding the field, assuming 1/8 of maximum potential yield.
				self.__workers_worked += 2
				return total_harvest
			#returns the total harvest of the field and increases workers workerd by two
			else:
				return 0

		'''Determines the distance between the associated household and respective field'''
		def findDistance(self, field):
			cor1 = field.findCoordinates()
			cor2 = self.__household.getCoordinates()
			hor = math.pow((cor1[0]-cor2[0]),2)
			ver = math.pow((cor1[1]-cor2[1]),2)
			distance = math.sqrt(hor + ver)
			#uses distance formula to determine the distance
			return distance
