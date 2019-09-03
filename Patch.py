import math
class Patch:

	#Attributes


	def __init__(self, patch_id, isField):
		self.__isSettlement = False
		self.__isRiver = False
		self.__isOwned = False
		self.__colour = "Yellow"
		self.__patch_id = patch_id
		self.__isField = isField
		if self.__isField == True:
			self.inner = self.Field(patch_id, 0)




	def getID(self):
		return self.__patch_id

	def findCoordinates(self):
		r = math.floor(self.__patch_id/41)
		c = self.__patch_id % 41
		return [r,c]

	def toggleSettlement(self):
		self.__isSettlement =  not self.__isSettlement

	def toggleField(self):
		self.__isField = not self.__isField

	def toggleRiver(self):
		self.__isRiver = not self.__isRiver

	def toggleOwned(self):
		self.__isOwned = not self.__isOwned

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

		#Attributes
		__field_id = 0
		__fertility = 0
		__avg_fertility = 0
		__harvested = False


		def __init__(self, field_id, fertility):
			self.__field_id = field_id
			self.__fetility = 5
			self.__years_fallow = 0

		def getFertility(self):
			return self.__fertility

		def toggleHarvested(self):
			self.__harvested = not self.__harvested

		def fieldChangeover(self):
			if(self.__harvested == True):
				self.__years_fallow = 0
			else:
				self.__years_fallow += 1
			return self.__years_fallow

		def updateHousehold():
			return 0
