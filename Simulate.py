import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
from PyQt5.QtGui import QPixmap, QPainter
import matplotlib.patches as ptc
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
from matplotlib.cbook import get_sample_data
#from matplotlib.widgets import Slider, Button, RadioButtons
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, \
	QTabWidget, QScrollArea, QFormLayout, QLabel, QSlider, QRadioButton, QGridLayout, QCheckBox, QPushButton, QDesktopWidget, QAbstractButton
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys
import threading
import random
from Map import Map
from Settlement import Settlement
from Household import Household
from Patch import Patch

mpl.use('Qt5Agg')

class PicButton(QAbstractButton):
	def __init__(self, pixmap, parent=None):
		super(PicButton, self).__init__(parent)
		self.pixmap = pixmap

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.drawPixmap(event.rect(), self.pixmap)

	def sizeHint(self):
		return self.pixmap.size()

class Simulate(QtWidgets.QMainWindow):
	#Attributes
	global c_id
	fig, ax = plt.subplots(figsize=(15,8.2))
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
	__household_List= np.empty(250, dtype= Household) #List of all Household objects
	#__settlement_List = np.empty(21, dtype= Settlement) #List of all Settlement objects
	__settlement_List = []
	coordinates = []
	#qapp = QtWidgets.QApplication([])
	#x, y = np.empty(20, dtype= int)
	#__grid = np.random.randint(10, size= (40,40))
	map = Map()

	def clearAll():
		#clear all method
		self.__model_time_span = 0
		self.__starting_settlements = 0
		self.__starting_households = 0
		self.__starting_household_size = 0
		self.__starting_grain = 0
		self.__min_competency = 0.0
		self.__min_ambition= 0.0
		self.__generation_variation = 0.0
		self.__knowledge_radius = 0
		self.__distance_cost = 0
		self.__fallow_limit = 0
		self.__pop_growth_rate = 0.0
		self.__allow_household_fission = False
		self.__min_fission_chance = 0.0
		self.__allow_land_rental = False
		self.__rental_rate = 0.0
		self.__projected_historical_population = 0
		self.__household_List= np.empty(250, dtype= Household) #List of all Household objects
		self.__settlement_List = np.empty(21, dtype= Settlement) #List of all Settlement objects
		self.map = Map()
		#WILL ALSO NEED TO CLEAR THE NUMPY ARRAY AND THE VISUALS

	def resetTicks():
		#resetTicks
		pass

	def setUpPatches(self):
		self.map.createPatches()

	def setUpSettlements(self):
		#MAP
		self.map = Map()
		s_id=0
		for i in range(self.__starting_settlements):
			s_id+=1
			s = Settlement(s_id,(self.__starting_households*self.__starting_household_size), self.__starting_households )
			#self.__settlement_List[i] = s
			self.__settlement_List.append(s)
			s.setHouseholds(self.setUpHouseholds(s)) #calls method in settlement class to set households in the settlement
		self.coordinates = self.map.setUpSettlements(self.__settlement_List)

	def setUpHouseholds(self, settle):
		#MAP
		households_for_settlement = np.empty(self.__starting_households, dtype = Household)
		for i in range(self.__starting_households):
			c_id = self.c_id+1
			h = Household(c_id, settle, self.__starting_household_size, self.__min_competency, self.__min_ambition, self.__knowledge_radius)
			self.__household_List[i] = h
			households_for_settlement[i] = h

		return households_for_settlement

	def createRiver(self):
		#need to set 2 columns of the Map to river
		#this means setting the Patch objects' attribute isRiver to true
		#and chanding the colour of the 2 columns to blue
		#this method will be called within the run simulation method
		self.map.createRiver()

	def establishPopulation(self):
		return self.__starting_settlements * self.__starting_households * self.__starting_household_size

	def populationShift():
		#popShift
		pass

	def removeHousehold(self, household):
		self.__household_List.delete(self.__household_List, [household], axis = 0)

	def fission():
		#fission
		pass

	def recolourHouseholds():
		#recolor
		pass

	def updatePlotValues():
		#need clarification on this method
		pass

	def calcTotalAmbition(self):
		pass

	def calcTotalCompetency():
		#competency
		pass

	def calcTotalPopulation():
		return self.__starting_settlements * self.__starting_households * self.__starting_household_size

	def saveUserInput(self, time, settlements, households, household_size, grain, comp, amb, gen_var,
		knowledge, dist, fallow, pop_growth, allow_fission, fission_chance, allow_rent, rent_rate):
		self.c_id = 0
		self.__model_time_span = time
		self.__starting_settlements = settlements
		self.__starting_households = households
		self.__starting_household_size = household_size
		self.__starting_grain = grain
		self.__min_competency = comp
		self.__min_ambition= amb
		self.__generation_variation = gen_var
		self.__knowledge_radius = knowledge
		self.__distance_cost = dist
		self.__fallow_limit = fallow
		self.__pop_growth_rate = pop_growth
		self.__allow_household_fission = allow_fission
		self.__min_fission_chance = fission_chance
		self.__allow_land_rental = allow_rent
		self.__rental_rate = rent_rate

		self.setUpPatches()
		self.setUpSettlements()
		self.createRiver()
		self.establishPopulation()

		for i in self.coordinates:
			self.ax.plot(i[0], i[1], marker="p") 

		self.runSimulation()


	def runSimulation(self):
		#arr = np.random.randint(1, size= (41,41)) #making it all yellow from the beginning

		cmap = mpl.colors.ListedColormap(['blue', 'lightgreen'])
		#bounds = [1,2]
		#norm = colors.BoundaryNorm(bounds,cmap.N)
		plt.rcParams['toolbar'] = 'None' #removes the toolbar


		if 1:
			#fig, ax = plt.subplots(figsize=(15,8.2))
			self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")
			#np.set_printoptions(threshold=sys.maxsize)
			#print(self.map.getGrid())

			#plt.subplots_adjust(left = 0.4)#adds space to the right of the plot

			# Define a 1st position to annotate (display it with a marker)
			xy = (23, 40)
			#ax.plot(xy[0], xy[1], "ro-")
			import threading
			import time

			lock = threading.Lock()
			farmCoordinates = []
			def a():
				count =0
				while(count<self.__model_time_span):
					lock.acquire()
					try:
						count += 1
						#print(count)
						for i in range(len(self.__settlement_List)):
							for j in range(len(self.__settlement_List[i].getHouseholdList())):
								#print(self.__settlement_List[i].getHouseholdList()[j])
								#farmCoordinates.append(self.__settlement_List[i].getHouseholdList()[j].claimFields(self.__settlement_List[i].getCoordinates()[0],self.__settlement_List[i].getCoordinates()[1]))
								#self.ax.plot(farmCoordinates[][0], farmCoordinates[k][1], '-ro')
								x = self.__settlement_List[i].getHouseholdList()[j].claimFields(self.__settlement_List[i].getCoordinates()[0],self.__settlement_List[i].getCoordinates()[1])
								print(x[0],x[1])
								self.ax.plot(x[0], x[1], '-rs')

					finally:
						time.sleep(0.1)
						lock.release()

			t = threading.Thread(name='a', target=a)

			t.start()
			
			# Annotate the 1st position with a text box ('Test 1')
			'''
			offsetbox = TextArea("Test 1", minimumdescent=False)
			ab = AnnotationBbox(offsetbox, xy,
								xybox=(-60, 40),
								xycoords='data',
								boxcoords="offset points",
								arrowprops=dict(arrowstyle="->"))
			ax.add_artist(ab)wai
			'''
			# Annotate the 1st position with another text box ('Test')
			'''
			offsetbox = TextArea("Test", minimumdescent=False)
			ab = AnnotationBbox(offsetbox, xy,
								xybox=(1.02, xy[1]),
								xycoords='data',
								boxcoords=("axes fraction", "data"),
								box_alignment=(0., 0.5),
								arrowprops=dict(arrowstyle="->"))
			ax.add_artist(ab)
			
			# Define a 2nd position to annotate (don't display with a marker this time)
			xy = [10, 4]
			# Annotate the 2nd position with a circle patch
			da = DrawingArea(20, 20, 0, 0)
			p = Circle((10, 10), 10)
			da.add_artist(p)
			ab = AnnotationBbox(da, xy,
								xybox=(1.02, xy[1]),
								xycoords='data',
								boxcoords=("axes fraction", "data"),
								box_alignment=(0., 0.5),
								arrowprops=dict(arrowstyle="->"))
			self.ax.add_artist(ab)
			# Annotate the 2nd position with an image (a generated array of pixels)
			arr = np.arange(1600).reshape((40, 40))
			im = OffsetImage(arr, zoom=1)
			im.image.axes = self.ax
			ab = AnnotationBbox(im, xy,
								xybox=(-40., 50.),
								xycoords='data',
								boxcoords="offset points",
								pad=0.3,
								arrowprops=dict(arrowstyle="->"))
			self.ax.add_artist(ab)
			# Annotate the 2nd position with another image
			fn = get_sample_data('/Users/user/Desktop/CSC3003S/EGYPT/Egypt_Simulation/settlement_yellow.png', asfileobj=False)
			arr_img = plt.imread(fn, format='png')
			imagebox = OffsetImage(arr_img, zoom=0.6)
			imagebox.image.axes = self.ax
			ab = AnnotationBbox(imagebox, xy,
								xybox=(120., -80.),
								xycoords='data',
								boxcoords="offset points",
								pad=0.5,
								arrowprops=dict(
									arrowstyle="->",
									connectionstyle="angle,angleA=0,angleB=90,rad=3")
								)
			self.ax.add_artist(ab)
			self.ax.grid(which='major', axis='both', linestyle='-', color='0', linewidth=0)
			'''

			#UNCOMMENT BELOW IF YOU WANT TO INVERT THE DIMENSIONS (EITHER 0 TO 40 OR 40 TO 0)
			#ax.set_xlim(0, 42)
			#ax.set_ylim(42, 0)

			major_ticks = np.arange(-1, 42, 1)
			minor_ticks = np.arange(0, 42, 1)
			self.ax.set_xticks(major_ticks)
			#ax.set_xticks(minor_ticks, minor=True)
			self.ax.set_yticks(major_ticks)
			#ax.set_yticks(minor_ticks, minor=True)

			#REMOVE THE AXES LABELS AND TICKS
			'''
			ax.set_yticklabels([])
			ax.set_xticklabels([])
			plt.xticks([])
			plt.yticks([])
			'''
			self.ax.axis('off') #comment out if you want to see the axis

			self.QWindow(self.fig)
			#plt.show()

	def main(self):
		#Main METHOD
		print("Simulation running"+str(self.__starting_settlements))
		#threadLock = threading.Lock()
		#with threadLock:
		#	global_counter += 1
	
	def QWindow(self, fig):
		#self.qapp = QtWidgets.QApplication([])

		QtWidgets.QMainWindow.__init__(self)
		self.widget = QtWidgets.QWidget()
		self.setCentralWidget(self.widget)
		vBoxLayout= QtWidgets.QVBoxLayout()
		self.widget.setLayout(vBoxLayout)
		self.widget.layout().setContentsMargins(0,0,0,0)
		self.widget.layout().setSpacing(0)

		self.fig = fig
		self.canvas = FigureCanvas(self.fig)
		self.canvas.draw()
		#self.scroll = QtWidgets.QScrollArea(self.widget)
		#self.scroll.setWidget(self.canvas)

		#self.nav = NavigationToolbar(self.scroll, self.widget)
		#self.widget.layout().addWidget()
		self.widget.layout().addWidget(self.canvas)

		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)

		#################### BUTTONS ####################
		btnSettings = PicButton(QPixmap('/Users/user/Desktop/CSC3003S/EGYPT/Egypt_Simulation/settings_pic.png'),self)
		btnSettings.move(5, 5)
		btnSettings.resize(50,50)
		btnSettings.clicked.connect(self.on_click_Settings)

		btnSetUp = QtWidgets.QPushButton('Set Up', self)
		btnSetUp.setToolTip('To set up/restart the simulation')
		btnSetUp.move(90,30)
		btnSetUp.clicked.connect(self.on_click_SetUp)

		btnStart = QtWidgets.QPushButton('Start', self)
		btnStart.setToolTip('Start the simulation')
		btnStart.move(185,30)
		btnStart.clicked.connect(self.on_click_Start)

		btnPause = QtWidgets.QPushButton('Pause', self)
		btnPause.setToolTip('Pause the simulation')
		btnPause.move(280,30)
		btnPause.clicked.connect(self.on_click_Pause)
		##################################################

		#THE MAIN WINDOW
		self.setGeometry(100,100,700,1200)
		self.setWindowTitle("Egypt Simulation")

		self.show()
		#exit(self.qapp.exec_())


	######ACTION FOR BUTTONS######
	def on_click_SetUp(self):
		print("THIS IS WHERE ALL THE USER INPUT WILL BE RETRIEVED AND SENT TO THE MAP")

	def on_click_Pause(self):
		print("PAUSE ALL THREADS INCREMENTING THE YEARS/TICKS AND ALL OTHER DATA ALTERING THINGS")

	def on_click_Start(self):
		pass

	def on_click_Settings(self):
		#app = QApplication(sys.argv)
		#w = SetUpWindow()
		#w.show()
		pass
		#sys.exit(app.exec_())
##############################################################################################################################################################################
	
	class SetUpWindow(QWidget):

		def __init__(self, parent=None):
			super(QWidget, self).__init__(parent)
			#self.layout = QFormLayout(self)
			'''
			self.tabs = QTabWidget()
			self.tab1 = QWidget()
			self.tab2 = QScrollArea()
			self.tabs.addTab(self.tab1, 'Tab 1')
			self.tabs.addTab(self.tab2, 'Tab 2')
			'''
			self.tab1 = QScrollArea(self)
			content_widget = QWidget()
			self.tab1.setWidget(content_widget)
			flay = QFormLayout(content_widget)
			self.tab1.setWidgetResizable(True)
			self.tab1.setGeometry(0,0, 400, 640)

			self.lblTimeSpan = QLabel("Model Time Span: ",self)
			self.lblTimeSpan.setGeometry(54,115, 200, 30)

			self.sliderTS = QSlider(Qt.Horizontal, self)
			self.sliderTS.setGeometry(50, 135, 100, 30)
			self.sliderTS.valueChanged.connect(self.changeValueTS)
			self.sliderTS.setRange(100, 500)
			self.sliderTS.setValue(300)
			##### MANUAL SEED RADIO BUTTON #####
			self.rbtnManSeed = QCheckBox("Manual Seed", self)
			self.rbtnManSeed.setChecked(True)
			self.rbtnManSeed.move(50, 165)
			###################################
			##### STARTING NUMBER OF SETTLEMENTS #####
			self.lblSettlements = QLabel("Starting Settlements: ",self)
			self.lblSettlements.setGeometry(54,195, 200, 30)

			self.sliderSett = QSlider(Qt.Horizontal, self)
			self.sliderSett.setGeometry(50, 215, 200, 30)
			self.sliderSett.valueChanged.connect(self.changeValueSett)
			self.sliderSett.setRange(5, 20)
			self.sliderSett.setValue(8)
			##########################################
			##### STARTING NUMBER OF HOUSEHOLDS #####
			self.lblHouseholds = QLabel("Starting Households: ",self)
			self.lblHouseholds.setGeometry(54,245, 200, 30)

			self.sliderHouse = QSlider(Qt.Horizontal, self)
			self.sliderHouse.setGeometry(50, 265, 200, 30)
			self.sliderHouse.valueChanged.connect(self.changeValueHouse)
			self.sliderHouse.setRange(1, 10)
			self.sliderHouse.setValue(1)
			##########################################
			##### STARTING NUMBER OF HOUSE SIZE #####
			self.lblHSize = QLabel("People per Household: ",self)
			self.lblHSize.setGeometry(54,295, 200, 30)

			self.sliderHSize = QSlider(Qt.Horizontal, self)
			self.sliderHSize.setGeometry(50, 315, 200, 30)
			self.sliderHSize.valueChanged.connect(self.changeValueHSize)
			self.sliderHSize.setRange(1, 10)
			self.sliderHSize.setValue(1)
			self.sliderHSize.setTickInterval(1)
			self.sliderHSize.setSingleStep(1)
			##########################################
			##### STARTING GRAIN #####
			self.lblGrain = QLabel("Starting Grain: ",self)
			self.lblGrain.setGeometry(54,345, 200, 30)

			self.sliderGrain = QSlider(Qt.Horizontal, self)
			self.sliderGrain.setGeometry(50, 365, 200, 30)
			self.sliderGrain.valueChanged.connect(self.changeValueGrain)
			self.sliderGrain.setRange(100, 8000)
			self.sliderGrain.setValue(2300)
			self.sliderGrain.setTickInterval(100)
			self.sliderGrain.setSingleStep(100)
			##########################################
			##### MIN AMBITION #####
			self.lblAmbit = QLabel("Min Ambition: ",self)
			self.lblAmbit.setGeometry(54,395, 200, 30)

			self.sliderAmbit = QSlider(Qt.Horizontal, self)
			self.sliderAmbit.setGeometry(50, 415, 200, 30)
			self.sliderAmbit.valueChanged.connect(self.changeValueAmbit)
			self.sliderAmbit.setRange(0, 10)
			self.sliderAmbit.setValue(3)
			##########################################
			##### MIN COMPETENCY #####
			self.lblComp = QLabel("Min Competency: ",self)
			self.lblComp.setGeometry(54,445, 200, 30)

			self.sliderComp = QSlider(Qt.Horizontal, self)
			self.sliderComp.setGeometry(50, 465, 200, 30)
			self.sliderComp.valueChanged.connect(self.changeValueComp)
			self.sliderComp.setRange(0, 10)
			self.sliderComp.setValue(4)
			##########################################
			##### GENERATIONAL VARIATION #####
			self.lblGen = QLabel("Generational Variation: ",self)
			self.lblGen.setGeometry(54,495, 200, 30)

			self.sliderGen = QSlider(Qt.Horizontal, self)
			self.sliderGen.setGeometry(50, 515, 200, 30)
			self.sliderGen.valueChanged.connect(self.changeValueGen)
			self.sliderGen.setRange(0, 10)
			self.sliderGen.setValue(3)
			##########################################
			##### KNOWLEDGE RADIUS #####
			self.lblKnow = QLabel("Knowledge Radius: ",self)
			self.lblKnow.setGeometry(54,545, 200, 30)

			self.sliderKnow = QSlider(Qt.Horizontal, self)
			self.sliderKnow.setGeometry(50, 565, 200, 30)
			self.sliderKnow.valueChanged.connect(self.changeValueKnow)
			self.sliderKnow.setRange(5, 40)
			self.sliderKnow.setValue(15)
			##########################################
			##### DISTANCE COST #####
			self.lblDist = QLabel("Distance Cost: ",self)
			self.lblDist.setGeometry(54,595, 200, 30)

			self.sliderDist = QSlider(Qt.Horizontal, self)
			self.sliderDist.setGeometry(50, 615, 200, 30)
			self.sliderDist.valueChanged.connect(self.changeValueDist)
			self.sliderDist.setRange(1, 25)
			self.sliderDist.setValue(6)
			##########################################
			##### FALLOW LIMIT  #####
			self.lblFLimit = QLabel("Fallow Limit: ",self)
			self.lblFLimit.setGeometry(54,595, 200, 30)

			self.sliderFLimit = QSlider(Qt.Horizontal, self)
			self.sliderFLimit.setGeometry(50, 615, 200, 30)
			self.sliderFLimit.valueChanged.connect(self.changeValueFLimit)
			self.sliderFLimit.setRange(0, 25)
			self.sliderFLimit.setValue(6)
			##########################################
			##### POP GROWTH #####
			self.lblPop = QLabel("Population Growth Rate: ",self)
			self.lblPop.setGeometry(54,595, 200, 30)

			self.sliderPop = QSlider(Qt.Horizontal, self)
			self.sliderPop.setGeometry(50, 615, 200, 30)
			self.sliderPop.valueChanged.connect(self.changeValuePop)
			self.sliderPop.setRange(0, 5)
			self.sliderPop.setValue(3)
			##########################################
			##### ALLOW FISSION #####
			self.rbtnFission = QCheckBox("Allow Household Fission", self)
			self.rbtnFission.setChecked(True)
			self.rbtnFission.move(50, 165)
			###################################
			##### POP GROWTH #####
			self.lblMinF = QLabel("Min Fission Chance: ",self)
			self.lblMinF.setGeometry(54,595, 200, 30)

			self.sliderMinF = QSlider(Qt.Horizontal, self)
			self.sliderMinF.setGeometry(50, 615, 200, 30)
			self.sliderMinF.valueChanged.connect(self.changeValueMinF)
			self.sliderMinF.setRange(5, 9)
			self.sliderMinF.setValue(3)
			##########################################
			##### ALLOW FISSION #####
			self.rbtnRental = QCheckBox("Allow Land Rental: ", self)
			self.rbtnRental.setChecked(True)
			self.rbtnRental.move(50, 165)
			###################################
			##### POP GROWTH #####
			self.lblRentalR = QLabel("Land Rental Rate: ",self)
			self.lblRentalR.setGeometry(54,595, 200, 30)

			self.sliderRentalR = QSlider(Qt.Horizontal, self)
			self.sliderRentalR.setGeometry(50, 615, 200, 30)
			self.sliderRentalR.valueChanged.connect(self.changeValueRentalR)
			self.sliderRentalR.setRange(30, 60)
			self.sliderRentalR.setValue(40)

			flay.addRow(self.lblTimeSpan)
			flay.addRow(self.sliderTS)

			flay.addRow(self.rbtnManSeed)

			flay.addRow(self.lblSettlements)
			flay.addRow(self.sliderSett)

			flay.addRow(self.lblHouseholds)
			flay.addRow(self.sliderHouse)

			flay.addRow(self.lblHSize)
			flay.addRow(self.sliderHSize)

			flay.addRow(self.lblGrain)
			flay.addRow(self.sliderGrain)

			flay.addRow(self.lblAmbit)
			flay.addRow(self.sliderAmbit)

			flay.addRow(self.lblComp)
			flay.addRow(self.sliderComp)

			flay.addRow(self.lblGen)
			flay.addRow(self.sliderGen)

			flay.addRow(self.lblKnow)
			flay.addRow(self.sliderKnow)

			flay.addRow(self.lblDist)
			flay.addRow(self.sliderDist)

			flay.addRow(self.lblFLimit)
			flay.addRow(self.sliderFLimit)

			flay.addRow(self.lblPop)
			flay.addRow(self.sliderPop)

			flay.addRow(self.rbtnFission)

			flay.addRow(self.lblMinF)
			flay.addRow(self.sliderMinF)

			flay.addRow(self.rbtnRental)

			flay.addRow(self.lblRentalR)
			flay.addRow(self.sliderRentalR)

			self.btnSU = QPushButton('Set Up', self)
			self.btnSU.setToolTip('To set up the simulation')
			self.btnSU.move(306,646)
			self.btnSU.clicked.connect(self.on_click_SU)

			#self.tab1.move(50,50)
			#self.layout.addWidget(self.btnSU)
			self.resize(400, 700)

			p = self.palette()
			p.setColor(self.backgroundRole(), Qt.white)
			self.setPalette(p)
			self.setWindowTitle("Set Up Simulation")

			#self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

			#SET THE SETUP WINDOW TO THE CENTER OF THE MAIN WINDOW
			#qtRectangle = self.frameGeometry()
			#centerPoint = QDesktopWidget().availableGeometry().center()
			#qtRectangle.moveCenter(centerPoint)
			#self.move(qtRectangle.topLeft())

			#self.activateWindow()

		#def setUserInput(self):
			#userInput = np.array([self.sliderTS.value(),self.rbtnManSeed.isChecked(),self.sliderSett.value(), self.sliderHouse.value(), self.sliderHSize.value(),self.sliderGrain.value(),
			#	self.sliderAmbit.value()/10,self.sliderGen.value()/10,self.sliderKnow.value(), self.sliderDist.value(), self.sliderFLimit.value(), self.sliderPop.value()/10,
			#	self.rbtnFission.isChecked() ,self.sliderMinF.value()/10, self.rbtnRental.isChecked() ,self.sliderRentalR.value()])
			#return userInput

		def on_click_SU(self):
			#get all the user input
			#	def saveUserInput(self, time, settlements, households, household_size, grain, comp, amb, gen_var,
		#knowledge, dist, fallow, pop_growth, allow_fission, fission_chance, allow_rent, rent_rate):
		#,self.rbtnManSeed.isChecked() - NEED TO CHECK IF WE STILL DOING THIS
			Simulate().saveUserInput(self.sliderTS.value(), self.sliderSett.value(), self.sliderHouse.value(), self.sliderHSize.value(), self.sliderGrain.value(), self.sliderComp.value()/10, \
				self.sliderAmbit.value()/10, self.sliderGen.value()/10, self.sliderKnow.value(), self.sliderDist.value(), self.sliderFLimit.value(), self.sliderPop.value()/10, self.rbtnFission.isChecked(), \
				self.sliderMinF.value()/10, self.rbtnRental.isChecked(), self.sliderRentalR.value())


		def changeValueTS(self):
			value = str(self.sliderTS.value())
			self.lblTimeSpan.setText("Model Time Span: "+ value)

		def changeValueSett(self):
			value = str(self.sliderSett.value())
			self.lblSettlements.setText("Starting Settlements: "+value)

		def changeValueHouse(self):
			value = str(self.sliderHouse.value())
			self.lblHouseholds.setText("Starting Households: "+value)

		def changeValueHSize(self):
			value = str(self.sliderHSize.value())
			self.lblHSize.setText("People per Household: "+value)

		def changeValueGrain(self):
			value = str(self.sliderGrain.value())
			self.lblGrain.setText("Starting Grain: "+value)

		def changeValueAmbit(self):
			value = str(self.sliderAmbit.value()/10)
			self.lblAmbit.setText("Min Ambition: "+value)

		def changeValueComp(self):
			value = str(self.sliderComp.value()/10)
			self.lblComp.setText("Min Competency: "+value)

		def changeValueGen(self):
			value = str(self.sliderGen.value()/10)
			self.lblGen.setText("Generational Variation: "+value)

		def changeValueKnow(self):
			value = str(self.sliderKnow.value())
			self.lblKnow.setText("Knowledge Radius: "+value)

		def changeValueDist(self):
			value = str(self.sliderDist.value())
			self.lblDist.setText("Distance Cost: "+value+" kg")

		def changeValueFLimit(self):
			value = str(self.sliderFLimit.value())
			self.lblFLimit.setText("Fallow Limit: "+value+" years")

		def changeValuePop(self):
			value = str(self.sliderPop.value()/10)
			self.lblPop.setText("Population Growth Rate: "+value+"%")

		def changeValueMinF(self):
			value = str(self.sliderMinF.value()/10)
			self.lblMinF.setText("Min Fission Chance: "+value)

		def changeValueRentalR(self):
			value = str(self.sliderRentalR.value())
			self.lblRentalR.setText("Rental Rate: "+value+"%")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = Simulate().SetUpWindow()
	w.show()

	#qapp = QtWidgets.QApplication([])
	#s = Simulate()
	#s.main()
	#s.runSimulation()

	sys.exit(app.exec_())
	#sys.exit(qapp.exec_())
