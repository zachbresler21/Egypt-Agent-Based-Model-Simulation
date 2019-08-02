class Patch(object):

	#Attributes
	__patch_id = 0
	__isSettlement = False
	__isField = False
	__isRiver = False
	__isOwned = False
	__colour = ""

	"""docstring for Patch"""
	def __init__(self, arg):
		super(Patch, self).__init__()
		self.arg = arg

	def setUpPatches():
		#SET UP

	class Field(object):

		#Attributes
		__field_id = 0
		__fetility = 0
		__avg_fertility = 0
		__harvested = False
		__years_fallow = 0

		"""docstring for Field"""
		def __init__(self, arg):
			super(Field, self).__init__()
			self.arg = arg
			
		def fieldChangeover():
			#

		def updateHousehold():
			#