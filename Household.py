from Patch import Patch
#import Settlement
from Map import Map
import random
import numpy as np
import math


class Household:

	#Attributes
	__knowledge_radius = 0
	#__belongingSettlement = Settlement
	map = Map()


	"""docstring for Household"""
	def __init__(self, h_id, coords, size,tot_grain, houseColour, fields_owned, fields_harvested, competency, ambition, rental_rate, allow_land_rental, distance_cost):

		self.__id = h_id
		#self.__belongingSettlement = settle
		self.__coordinates = coords
		self.__size = size
		self.__tot_grain = tot_grain

		self.__houseColour = houseColour
		self.__generationCountdown = 0
		self.__distance_cost = 0
		self.__allow_land_rental = False
		self.__rental_rate = 0
		self.__fields_owned = fields_owned
		self.__fields_harvested = fields_harvested
		self.map = Map()

		self.__competency =  competency + (random.random()*(1-competency))
		self.__ambition = ambition + (random.random()*(1-ambition))

		self.__inner = self.Farm(self)

	def __init__(self, h_id, coords, size, competency, ambition, know_radius):
		self.__id = h_id
		#self.__belongingSettlement = settle
		self.__coordinates = coords
		self.__knowledge_radius = know_radius
		self.__size = size
		self.__ambtion = ambition
		self.__competency = competency
		self.__tot_grain = 0
		self.__colour = "Grey"
		self.__generationCountdown = 0
		self.__distance_cost = 0
		self.__allow_land_rental = False
		self.__rental_rate = 0.0
		self.__fields_owned = [] #list of Field objects
		self.__fields_harvested = [] #list of Field objects

		self.map = Map()

		self.__competency =  competency + (random.random()*(1-competency))
		self.__ambition = ambition + (random.random()*(1-ambition))

		self.inner = self.Farm(self)


	def getFieldsOwned(self):
		return self.__fields_owned

	def getSize(self):
		return self.__size

	def getCompetency(self):
		return self.__competency

	def getAmbition(self):
		return self.__ambition

	def getCoordinates(self):
		return self.__coordinates

	def getTotGrain(self):
		return self.__tot_grain

	def addTotGrain(self,tot_harvest):
		self.__tot_grain += tot_harvest

	def addHarvestField(self, field):
		self.__fields_harvested.append(field)

	def removeField(self,field):
		self.__fields_owned.remove(field)

	def setCoordinates(self,coords):
		self.__coordinates = coords

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

	def getID(self):
		return self.__id

	def claimFields(self, row, col):
		#
		patches = self.map.getPatches()
		claim_chance = random.uniform(0,1) #creates a random float between 0 and 1
		if (self.__size > len(self.__fields_owned) or len(self.__fields_owned) <= 1): #checks if household will be trying to claim land ADD LATER(claim_chance < self.__ambition) and
			current_grain = self.__tot_grain
			claim_field = Patch(34567, True)
			best_fertility = 0

			r = np.arange(0, 41)
			c = np.arange(0, 41)

			cr = row
			cc = col
			radius = self.__knowledge_radius

			#determines indices in the circle with knowledge radius
			mask = (r[np.newaxis,:]-cr)**2 + (c[:,np.newaxis]-cc)**2 < radius**2

			for patch in patches[mask]: #traverses through array of patches in the circle
				if patch.isField()==True and patch.isOwned() == False and patch.isRiver() == False and patch.isSettlement() == False:
					#fertility = patch.Field().getFertility()
					fertility = 5
					if fertility > best_fertility: #finds field with best fertility
						best_fertility = fertility
						claim_field = patch

			x = self.completeClaim(claim_field)
			#print(x)
			return x


	def completeClaim(self, claim_field):
		claim_field.toggleOwned()
		self.__fields_owned.append(claim_field)
		return claim_field.findCoordinates()

	def rentLand():
		#
		pass

	def consumeGrain(self):
		self.__tot_grain = self.__tot_grain - (self.__size*160) #workers consuming 160kg of grain a year
		if self.__tot_grain <= 0: #if not enough grain to feed workers, one dies
			self.__tot_grain = 0
			self.__size = self.__size - 1
			return True
		return False

	def checkWorkers(self):
		if(self.__size <= 0): #if no workers left: change households field to unowned and remove household from settlement
			for field in self.__fields_owned:
				field.toggleOwned
			return True
		return False


	def storageLoss():
		self.__tot_grain = self.__tot_grain - (self.__tot_grain*0.1)

	def populationShift():
		#
		pass
	'''
	def removeMember():
		self.__size = self.__size - 1
		if self.__size == 0:
			self.__belongingSettlement.removeHousehold()
	'''
	def addMember(self):
		self.__size = self.__size + 1

	def beginFarm():
		#
		pass

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


	def removeFields():
		#
		pass

	class Farm:

		#Attributes
		__max_potential_yield = 2475

		def __init__(self, household):
			self.__best_harvest = 0
			self.__workers_worked = 0
			self.__household = household


		def beginFarm(self, distance_cost):
			best_field = self.determineField(distance_cost)
			total_harvest = self.calcYield(best_field)
			self.__household.addTotGrain(total_harvest)
			self.__household.addHarvestField(best_field)


		def determineField(self,distance_cost):
			num_harvests = math.floor(self.__household.getSize() / 2) #one harvest for every 2 workers
			self.__best_harvest = 0
			best_field = Patch(34567, True)
			for i in range(num_harvests):
				for field in self.__household.getFieldsOwned(): #fields_owned is an array of patches
					this_harvest = (field.inner.getFertility()*self.__max_potential_yield*self.__household.getCompetency())-(self.findDistance(field)*distance_cost)
					#yield dependent on fertility, whether or not the household actually farms the field (competency) and distance cost
					if(field.inner.isHarvested() == False and this_harvest > self.__best_harvest): #finds highest yield field
						self.__best_harvest = this_harvest
						best_field = field
			return best_field


		def calcYield(self,field):
			#takes a Field object as a parameter
			farm_chance = random.uniform(0,1) #creates a random float between 0 and 1
			if(self.__household.getTotGrain() < (self.__household.getSize() * 160) or farm_chance < (self.__household.getAmbition() * self.__household.getCompetency())):
				#160 is kilograms of grain per person annually, after Hassan 1984, 63.
				field.inner.toggleHarvested() #NEED TO TOGGLE FIELDS HARVESTED EVERY TICK
				#Change shape? Show harvest on the plot?
				total_harvest = self.__best_harvest - 300  #300 = cost of seeding the field, assuming 1/8 of maximum potential yield.
				self.__workers_worked += 2
				return total_harvest
			else:
				return 0


		def findDistance(self, field):
			#determines distance between household and field
			cor1 = field.findCoordinates()
			cor2 = self.__household.getCoordinates()
			hor = math.pow((cor1[0]-cor2[0]),2)
			ver = math.pow((cor1[1]-cor2[1]),2)

			#distance = math.sqrt(hor + ver)
			distance = 0
			return distance
