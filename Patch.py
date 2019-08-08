class Patch():


	#Attributes
	__patch_id = 0
	__isSettlement = False
	__isField = False
	__isRiver = False
	__isOwned = False
	__colour = "Yellow"

	def __init__(self, patch_id, isField):
		self.__patch_id = patch_id
		self.__isField = isField
		if self.__isField == True:
			self.inner = self.Field(patch_id, 0.8, 0)

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



	class Field:

		#Attributes
		__field_id = 0
		__fetility = 0
		__avg_fertility = 0
		__harvested = False
		__years_fallow = 0

		def __init__(self, field_id, fertility, years_fallow):
			self.__field_id = field_id
			self.__fetility = fertility
			self.__years_fallow = years_fallow

		def toggleHarvested(self):
			self.__harvested = not self.__harvested;

		def fieldChangeover():
			return 0

		def updateHousehold():
			return 0
