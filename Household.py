from Patch import Patch
#import Settlement
from Map import Map
import random
import numpy as np
import math


class Household:

	#Attributes
	__knowledge_radius = 0
	map = Map()


	"""docstring for Household"""
	def __init__(self, h_id, size,tot_grain, competency, ambition, rental_rate, allow_land_rental, distance_cost, knowledge_radius):

		self.__id = h_id
		self.__size = size
		self.__tot_grain = tot_grain
		self.__generationCountdown = random.randint(0,5)+10
		self.__distance_cost = distance_cost
		self.__allow_land_rental = allow_land_rental
		self.__rental_rate = rental_rate
		self.__knowledge_radius = knowledge_radius
		self.__fields_owned = []
		self.__coordinates = []
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

	def getDistanceCost(self):
		return self.__distance_cost

	def addTotGrain(self,tot_harvest):
		self.__tot_grain += tot_harvest

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
					fertility = patch.inner.getFertility()
					if fertility >= best_fertility: #finds field with best fertility
						best_fertility = fertility
						claim_field = patch

			x = self.completeClaim(claim_field)
			#print(x)
			return x


	def completeClaim(self, claim_field):
		claim_field.toggleOwned()
		self.__fields_owned.append(claim_field)
		return claim_field.findCoordinates()

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


	def addMember(self):
		self.__size = self.__size + 1

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

	def rentLand(self):
		patches = self.map.getPatches()

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
			if(patch.isField() and patch.inner.isHarvested() == False and this_harvest >= best_harvest): #finds highest yield field
				self.__best_harvest = this_harvest
				best_field = patch

		harvest_chance = random.uniform(0,1)
		if(harvest_chance < self.__ambition * self.__competency):
			best_field.inner.toggleHarvested()
			total_harvest += ((best_harvest * (1 - (self.__rental_rate / 100))) - 300)

		self.__tot_grain += total_harvest
		self.inner.clearWorkersWorked()


	class Farm:

		#Attributes
		__max_potential_yield = 2475

		def __init__(self, household):
			self.__best_harvest = 0
			self.__workers_worked = 0
			self.__household = household

		def getWorkersWorked(self):
			return self.__workers_worked

		def clearWorkersWorked(self):
			self.__workers_worked = 0

		def beginFarm(self):
			num_harvests = math.floor(self.__household.getSize() / 2) #one harvest for every 2 workers
			for i in range(num_harvests):
				best_field = self.determineField()
				total_harvest = self.calcYield(best_field)
				self.__household.addTotGrain(total_harvest)

		def determineField(self):
			self.__best_harvest = 0
			best_field = Patch(34567, True)
			for field in self.__household.getFieldsOwned(): #fields_owned is an array of patches
				this_harvest = (field.inner.getFertility()*self.__max_potential_yield*self.__household.getCompetency())-(self.findDistance(field)*self.__household.getDistanceCost())
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

			distance = math.sqrt(hor + ver)
			return distance
