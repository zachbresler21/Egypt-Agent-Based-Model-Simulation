import math
class Patch:

	#Attributes
	'''
	Constructor method
	'''
	def __init__(self, patch_id, isField):
		self.__isSettlement = False
		self.__isRiver = False
		self.__isOwned = False
		self.__colour = "Yellow"
		self.__patch_id = patch_id
		self.__isField = isField
		if self.__isField == True:
			self.inner = self.Field(patch_id)

	'''
	Gets the ID of the patch
	'''
	def getID(self):
		return self.__patch_id

	'''
	Find the coordinates of the patch
	'''
	def findCoordinates(self):
		r = math.floor(self.__patch_id/41)
		c = self.__patch_id % 41
		return [r,c]


	'''
	Toggles the isSettlement boolean value
	'''
	def toggleSettlement(self):
		self.__isSettlement =  not self.__isSettlement

	'''
	Toggles the isField boolean value
	'''
	def toggleField(self):
		self.__isField = not self.__isField

	'''
	Toggles the isRiver boolean value
	'''
	def toggleRiver(self):
		self.__isRiver = not self.__isRiver

	'''
	Toggles the isOwned boolean value
	'''
	def toggleOwned(self):
		self.__isOwned = not self.__isOwned

	'''
	Changes the colour of the patch
	'''
	def changeColour(self, colour):
		self.__colour = colour

	def isRiver(self):
		return self.__isRiver

	def isSettlement(self):
		return self.__isSettlement

	def isField(self):
		return self.__isField

	def isOwned(self):
		return self.__isOwned

	def getFieldFertility(self):
		pass


	class Field:
		'''
		Constructor method
		'''
		def __init__(self, field_id):
			self.__field_id = field_id
			self.__fertility = 0
			self.__years_fallow = 0
			self.__harvested = False

		def getFertility(self):
			return self.__fertility

		def setFertility(self,fertility):
			self.__fertility = fertility

		def setHarvestFalse(self):
			self.__harvested = False

		def isHarvested(self):
			return self.__harvested

		'''
		Toggles the isHarvested boolean value
		'''
		def toggleHarvested(self):
			self.__harvested = not self.__harvested

		'''
		Allows a household to claim land owned by another household if that land has not been harvested for a certain amount of time (based on initial starting parameters)
		'''
		def fieldChangeover(self):
			if(self.__harvested == True):
				self.__years_fallow = 0
			else:
				self.__years_fallow += 1
			return self.__years_fallow
