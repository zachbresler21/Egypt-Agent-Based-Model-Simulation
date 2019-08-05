import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.patches as ptc
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
from matplotlib.cbook import get_sample_data
from matplotlib.widgets import Slider, Button, RadioButtons
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
mpl.use('Qt5Agg')

class Simulate(QtWidgets.QMainWindow):
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

	'''
	def clearAll():
		#clear all method

	def resetTicks():
		#resetTicks

	def setUpPatches():
		#MAP

	def setUpSettlements(self):
		#MAP
		for i in __starting_settlements:
			s = Settlement()
			self.__settlement_List.append(s)
			s.setHouseholds(setUpHouseholds()) #calls method in settlement class to set households in the settlement

	def setUpHouseholds(self):
		#MAP
		#returns a list of households per settlement to be used in setUpSettlements
		households_for_settlement = [] #List of households to be added to settlements
		for i in startingHouseholds:
			Household h = new Household()
			households_for_settlement.append(h)
			self.__household_List.append(h)

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
	'''

	def scrollableWindow(self, fig):
		self.qapp = QtWidgets.QApplication([])

		QtWidgets.QMainWindow.__init__(self)
		self.widget = QtWidgets.QWidget()
		self.setCentralWidget(self.widget)
		self.widget.setLayout(QtWidgets.QVBoxLayout())
		self.widget.layout().setContentsMargins(0,0,0,0)
		self.widget.layout().setSpacing(0)

		self.slider = QtWidgets.QSlider(Qt.Horizontal)

		self.fig = fig
		self.canvas = FigureCanvas(self.fig)
		self.canvas.draw()
		self.scroll = QtWidgets.QScrollArea(self.widget)
		self.scroll.setWidget(self.canvas)

		self.nav = NavigationToolbar(self.canvas, self.widget)
		self.widget.layout().addWidget(self.nav)
		self.widget.layout().addWidget(self.scroll)

		self.widget.layout().addWidget(self.slider, 20)

		#self.slider.setGeometry(30, 40, 200, 30)

		#vbox = QtWidgets.QVBoxLayout()
		#self.slider = QtWidgets.QSlider(Qt.Horizontal, self)
		#self.slider.setGeometry(30, 40, 200, 30)

		#vbox.addWidget(self.slider)
		#self.widget.layout().addWidget(self.slider)

		self.setGeometry(100,100,1200,1600)
		self.setWindowTitle("Egypt Simulation")

		self.show()
		exit(self.qapp.exec_()) 


	def runSimulation(self):
		arr = np.random.randint(10, size= (41,41))
		cmap = mpl.colors.ListedColormap(['yellow', 'green'])
		#bounds = [1,2,3 ]
		#norm = colors.BoundaryNorm(cmap.N)
		plt.rcParams['toolbar'] = 'None' #removes the toolbar at the bottom of the GUI
		
		if 1:
			fig, ax = plt.subplots(figsize=(14,7.2))
			ax.imshow(arr, cmap=cmap, interpolation= "None")

			plt.subplots_adjust(left = 0.4)#adds space to the right of the plot


			# Define a 1st position to annotate (display it with a marker)
			xy = (40, 40)
			ax.plot(xy[0], xy[1], ".r")

			# Annotate the 1st position with a text box ('Test 1')
			offsetbox = TextArea("Test 1", minimumdescent=False)

			ab = AnnotationBbox(offsetbox, xy,
								xybox=(-40, 40),
								xycoords='data',
								boxcoords="offset points",
								arrowprops=dict(arrowstyle="->"))
			ax.add_artist(ab)

			# Annotate the 1st position with another text box ('Test')
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

			ax.add_artist(ab)

			# Annotate the 2nd position with an image (a generated array of pixels)
			#arr = np.arange(1600).reshape((40, 40))
			im = OffsetImage(arr, zoom=1)
			im.image.axes = ax

			ab = AnnotationBbox(im, xy,
								xybox=(-40., 50.),
								xycoords='data',
								boxcoords="offset points",
								pad=0.3,
								arrowprops=dict(arrowstyle="->"))

			ax.add_artist(ab)

			# Annotate the 2nd position with another image
			fn = get_sample_data("/Users/user/Desktop/settlement_yellow.png", asfileobj=False)
			arr_img = plt.imread(fn, format='png')

			imagebox = OffsetImage(arr_img, zoom=0.6)
			imagebox.image.axes = ax

			ab = AnnotationBbox(imagebox, xy,
								xybox=(120., -80.),
								xycoords='data',
								boxcoords="offset points",
								pad=0.5,
								arrowprops=dict(
									arrowstyle="->",
									connectionstyle="angle,angleA=0,angleB=90,rad=3")
								)

			ax.add_artist(ab)
			ax.grid(which='major', axis='both', linestyle='-', color='0', linewidth=0)
			# Fix the display limits to see everything

			#UNCOMMENT BELOW IF YOU WANT TO INVERT THE DIMENSIONS (EITHER 0 TO 40 OR 40 TO 0)
			#ax.set_xlim(0, 40)
			#ax.set_ylim(0, 40)

			major_ticks = np.arange(0, 42, 1)
			minor_ticks = np.arange(0, 42, 1)
			ax.set_xticks(major_ticks)
			#ax.set_xticks(minor_ticks, minor=True)
			ax.set_yticks(major_ticks)
			#ax.set_yticks(minor_ticks, minor=True)




			#REMOVE THE AXES LABELS AND TICKS
			'''
			ax.set_yticklabels([])
			ax.set_xticklabels([])
			plt.xticks([])
			plt.yticks([])
			'''
			ax.axis('off') #comment out if you want to see the axis

			######################### USER INPUT #########################
			#SLIDERS
			

			#slider = QtWidgets.QSlider(Qt.Horizontal, self)
			#slider.setGeometry(30, 40, 200, 30)

			#slider.setFocusPolicy(Qt.StrongFocus)
			#slider.setTickPosition(QSlider.TicksBothSides)
			#slider.setTickInterval(10)
			#slider.setSingleStep(1)

			#BUTTONS
			
			self.scrollableWindow(fig)
			#plt.show()

	def main():
		#Main METHOD
		print("Simulation running")
		#Will get input from sliders later on
		#__starting_settlements = int(input("Enter starting settlements: "))
		#__starting_households = int(input("Enter starting households: "))

		#setUpSettlements()

	if __name__ == "__main__":
		main()


qapp = QtWidgets.QApplication([])
s = Simulate()
s.runSimulation()
