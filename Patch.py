import math

class Patch:

	'''Docstring for patch'''
	def __init__(self, patch_id, isField):
		self.__isSettlement = False
		self.__isRiver = False
		self.__isOwned = False
		self.__patch_id = patch_id
		self.__isField = isField
		if self.__isField == True:
			self.inner = self.Field(patch_id) #creates a Field object associated with the patch

	'''Gets the ID of the patch'''
	def getID(self):
		return self.__patch_id

	'''Determines the coordinates of the patch'''
	def findCoordinates(self):
		r = math.floor(self.__patch_id/41)
		c = self.__patch_id % 41
		return [r,c]
		#determines the coordinates of the patch from the patch ID and returns such coordinates

	'''Toggles the isSettlement boolean value'''
	def toggleSettlement(self):
		self.__isSettlement =  not self.__isSettlement

	'''Toggles the isField boolean value'''
	def toggleField(self):
		self.__isField = not self.__isField

	'''Toggles the isRiver boolean value'''
	def toggleRiver(self):
		self.__isRiver = not self.__isRiver

	'''Toggles the isOwned boolean value'''
	def toggleOwned(self):
		self.__isOwned = not self.__isOwned

	'''Returns whether the patch is a river or not'''
	def isRiver(self):
		return self.__isRiver

	'''Returns whether the patch is a settlement or not'''
	def isSettlement(self):
		return self.__isSettlement

	'''Returns whether the patch is a field or not'''
	def isField(self):
		return self.__isField

	'''Returns whether the patch is owned or not'''
	def isOwned(self):
		return self.__isOwned


	class Field:
		'''Field is a inner class of Patch'''

		'''Docstring for Field'''
		def __init__(self, field_id):
			self.__field_id = field_id
			self.__fertility = 0
			self.__years_fallow = 0
			self.__harvested = False

		'''Returns the fertility of the field'''
		def getFertility(self):
			return self.__fertility

		'''Sets the fertility of the field'''
		def setFertility(self,fertility):
			self.__fertility = fertility

		'''Sets harvested to false'''
		def setHarvestFalse(self):
			self.__harvested = False

		'''Returns whether the field is harvested or not'''
		def isHarvested(self):
			return self.__harvested

		'''Toggles the isHarvested boolean value'''
		def toggleHarvested(self):
			self.__harvested = not self.__harvested

		'''Allows fields that have lay fallow for a certain number of years to be forfeited for claim by other households'''
		def fieldChangeover(self):
			if(self.__harvested == True):
				self.__years_fallow = 0
			else:
				self.__years_fallow += 1
			return self.__years_fallow
