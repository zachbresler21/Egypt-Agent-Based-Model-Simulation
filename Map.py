import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.patches as ptc
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
from matplotlib.cbook import get_sample_data
from matplotlib.widgets import Slider, Button

class Map:
	#Attributes
	__lorenz_points = 0.0
	__gini_index_reserve = 0.0
	__avg_ambition = 0.0
	__avg_competency = 0.0
	__grid = np.empty((40,40), dtype= int) #list of patches

	def __init__ (self):
		self.__grid = np.random.randint(10, size= (40,40))


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

		    imagebox = OffsetImage(arr_img, zoom=1)
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

		    axSlider1 = plt.axes([0.03, 0.8, 0.2, 0.02])
		    timeSpanSlider = Slider(ax = axSlider1, label = "", valmin = 100, valmax = 500, valinit = 400, valfmt= '%1.0f',valstep = 10)
		    plt.text(100,2, "Model Time Span:", fontsize = 10, weight = "bold")


		    plt.show()
			

	'''def createRiver():
	

	def setUpSettlements(settlement_list):
		#takes a list of settlements as a parameter

	def assignFertilityColour(fertility):
		#takes a string as a parameter

	def claimField(household):
		#takes a Household object as a parameter

	def harvest():
		#harvest

	def rentField():
		#rent

	def removeLink():
		#remove

	def enlargeSettlement(factor):
		#takes an int as a parameter

	def reduceSettlement(factor):
		##takes an int as a parameter

	def recolourHouseholds():
		#recolour

	def updatePlotValues(totHouseholds, totPopulation, ambition, competency):
		#update - REVISE THE METHOD THAT IS IN THE SIMULATE CLASS

 
'''

mac = Map()
mac.runSimulation()
