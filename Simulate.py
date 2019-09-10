import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import matplotlib.image as mpimg
import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from sys import platform as sys_pf
if sys_pf == 'darwin':
	import matplotlib
	matplotlib.use("TkAgg")
import sys
import threading
import time
import random
import math
from Map import Map
from Settlement import Settlement
from Household import Household
from Patch import Patch

plt.style.use('ggplot')
'''This class is used for scrollpane wheere the user inputs are placed'''
class ScrollFrame(tk.Frame):

	def __init__(self, parent):
		super().__init__(parent) # create a frame (self)

		self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
		self.viewPort = tk.Frame(self.canvas, width=200, height=400 ,background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets
		self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self
		self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

		self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
		self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
		self.canvas.create_window((14,8), window=self.viewPort, anchor="nw",            #add view port frame to canvas
								  tags="self.viewPort")

		self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.

	def onFrameConfigure(self, event):
		'''Reset the scroll region to encompass the inner frame'''
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

class Simulate(tk.Frame):
	continuePlotting = False
	graphPlotting = False
	fig = plt.figure(figsize=(10,8.2))
	ax = fig.add_subplot(1,1,1)
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1,1,1)


	#totPop = plt.subplot2grid((6,2), (0,0), rowspan = 2 , colspan= 1)
	xList = []
	yList = []
	global c_id
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
	__allow_land_rental = False
	__rental_rate = 0.0
	__projected_historical_population = 0
	__total_population = 0
	__household_List= np.empty(250, dtype= Household) #List of all Household objects
	__settlement_List = []
	coordinates = []
	cv = fig
	cv2 = fig2
	#x, y = np.empty(20, dtype= int)
	#__grid = np.random.randint(10, size= (40,40))
	map = Map()
	x = []
	y = []

	def __init__(self, root):

		tk.Frame.__init__(self, root)
		self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
		'''
		# **********************************************************
		# 		               	User Inputs
		# The user input below is added to the scrollframe created above
		# **********************************************************
		'''
		self.count = 0
		mtp = tk.Scale(self.scrollFrame.viewPort, from_=100, to=500, orient=HORIZONTAL, label = "Model Time Span:", length = 180, resolution=50)
		mtp.pack(padx=20, pady=10, side=tk.TOP)
		mtp.set(100)

		ss = tk.Scale(self.scrollFrame.viewPort, from_=5, to=20, orient=HORIZONTAL, label = "Starting Settlements:", length = 180)
		ss.pack(pady = 10)
		ss.set(5)

		sh = tk.Scale(self.scrollFrame.viewPort, from_=1, to=10, orient=HORIZONTAL, label = "Starting Households:", length = 180)
		sh.pack()
		sh.set(3)

		shs = tk.Scale(self.scrollFrame.viewPort, from_=1, to=10, orient=HORIZONTAL, label = "Starting Household Size:", length = 180)
		shs.pack()
		shs.set(3)

		sg = tk.Scale(self.scrollFrame.viewPort, from_=100, to=8000, orient=HORIZONTAL, label = "Starting Grain:", length = 180)
		sg.pack()
		sg.set(3500)

		ma = tk.Scale(self.scrollFrame.viewPort, from_=0.0, to=1.0, orient=HORIZONTAL, label = "Min Ambition:", length = 180, resolution=0.1)
		ma.pack()
		ma.set(0.4)

		mc = tk.Scale(self.scrollFrame.viewPort, from_=0.0, to=1.0, orient=HORIZONTAL, label = "Min Competency:", length = 180, resolution=0.1)
		mc.pack()
		mc.set(0.5)

		gv = tk.Scale(self.scrollFrame.viewPort, from_=0.0, to=1.0, orient=HORIZONTAL, label = "Generation Variation:", length = 180, resolution=0.1)
		gv.pack()
		gv.set(0.2)

		kr = tk.Scale(self.scrollFrame.viewPort, from_=5, to=40, orient=HORIZONTAL, label = "Knowledge Radius:", length = 180)
		kr.pack()
		kr.set(15)

		dc = tk.Scale(self.scrollFrame.viewPort, from_=1, to=15, orient=HORIZONTAL, label = "Distance Cost (kg):", length = 180)
		dc.pack()
		sh.set(3)

		fl = tk.Scale(self.scrollFrame.viewPort, from_=0, to=50, orient=HORIZONTAL, label = "Fallow Limit:", length = 180)
		fl.pack()
		fl.set(17)

		pg = tk.Scale(self.scrollFrame.viewPort, from_=0, to=50, orient=HORIZONTAL, label = "Population Growth %:", length = 180)
		pg.pack()
		pg.set(20)

		varRent = IntVar()
		chkRent = tk.Checkbutton (self.scrollFrame.viewPort, text = "Land Rental" , padx = 0, pady = 2, variable = varRent)
		chkRent.pack()

		rr = tk.Scale(self.scrollFrame.viewPort, from_=0, to=10, orient=HORIZONTAL, label = "Rental Rate %:", length = 180)
		rr.pack()
		rr.set(5)
		# **********************************

		self.scrollFrame.pack(side=tk.LEFT, fill="both", expand=True)
		'''method that is activated by the click of the quit button - quits and destoys the program'''
		def _quit():
			root.quit()     # stops mainloop
			root.destroy()

		'''method that is activated by the click of the start button
		This method saves the user input and sets the respective variables'''
		def _start():

			rent = False

			if(varRent == 1):
				rent = True

			self.saveUserInput(mtp.get(), ss.get(), sh.get(), shs.get(), sg.get(), mc.get(), \
			ma.get(), gv.get(), kr.get(), dc.get(), fl.get(), pg.get(), rent, rr.get())

		'''
		# **********************************************************************************
		# 								 INFORMATION WINDOW
		#This window gives the user extra information about the simulation and how to use it
		# **********************************************************************************
		'''

		def _info():

			informationWindow = Toplevel()
			self.sf = ScrollFrame(informationWindow)
			informationWindow.title("Simulation Essential Information")
			h1 = tk.Label(self.sf.viewPort, text = "WHAT IS THIS?", bg= "lightblue", font = "calibri", fg = "black", bd = 10, width = 60)
			h1.pack()
			p1 = tk.Label(self.sf.viewPort, text = "\nAn abstraction of predynastic Nile valley (ca. 3700 BCE)\n\nModel allows one to see how they dynamics of variable Nile floods + chance + human\npersonality affect the accumulation of wealth and population distribution.\n", font = "calibri", fg = "black", bd = 10, width = 60, justify = LEFT)
			p1.pack()

			h2 = tk.Label(self.sf.viewPort, text = "HOW IT WORKS", bg= "lightblue", font = "calibri", fg = "black", bd = 10, width = 60)
			h2.pack()
			p2 = tk.Label(self.sf.viewPort, text = "\nAt the beginning of the run (setup), settlements are randomly distributed across the\nflood plain (but they are not allowed to be too close to each other - this is in the code)\n\nNotes about world setup:\n6km x 6km abstraction of the Nile valley\neach patch = 200m x 200m\nthus, in the code, max agricultural yield is set at 2450kg per patch according to\nhistorical data\n\nconsumption is set at 160kg per year according to historical data\n\nseeding cost set at 1/8 yield, rounded here to 300kg\n\n(what rules the agents use to create the overall behavior of the model)\n", font = "calibri", fg = "black", bd = 10, width = 60, justify = LEFT)
			p2.pack()

			h3 = tk.Label(self.sf.viewPort, text = "HOW TO USE IT", bg= "lightblue", font = "calibri", fg = "black", bd = 10, width = 60)
			h3.pack()
			p3 = tk.Label(self.sf.viewPort, text = "\nChanges can be made to the variables by interacting with the user input.\nOnce the user is happy with the variables they can then click the start button to start the simulation\n", font = "calibri", fg = "black", bd = 10, width = 60, justify = LEFT)
			p3.pack()

			self.sf.pack(fill="both", expand=True)
			informationWindow.geometry("600x700")
		# **********************************

		start = tk.Button(master=root, text="Start", command=_start)
		start.pack(in_ = self.scrollFrame, side=tk.LEFT)

		quit = tk.Button(master=root, text="Quit", command=_quit)
		quit.pack(in_ = self.scrollFrame, side=tk.LEFT)

		info = tk.Button(master=root, text="Info", command=_info)
		info.pack(in_ = self.scrollFrame, side=tk.RIGHT)

		self.scrollFrame.pack(side="top", fill="both", expand=True)

	'''Calls createPatches() in the Map class which will create a numpy array filled with Patch objects'''
	def setUpPatches(self):
		self.map.createPatches()

	'''Creates a number of settlement objects equal to the number entered in by the user.
	It adds these settlement objects to the settlement_list. Each settlement then sets up the
	household objects that will be associated with it. These Household objects will
	be stored in a list in the settlement class'''
	def setUpSettlements(self):
		self.map = Map()
		s_id=0
		for i in range(self.__starting_settlements):
			s_id+=1
			s = Settlement(s_id,(self.__starting_households*self.__starting_household_size), self.__starting_households, )
			self.__settlement_List.append(s)
			s.setHouseholds(self.setUpHouseholds(s)) #calls method in settlement class to set household_list in the settlement (returned from calling setUpHouseholds)
		self.coordinates = self.map.setUpSettlements(self.__settlement_List) #calls a method in map to randomly generate coordinates the settlement

	'''For each settlement created, setUpHouseholds method is called. This creates a number of household objects equal to the number
	of households entered in by the user. The method will then return a list of households which will be passed to the settlement created.'''
	def setUpHouseholds(self, settle):
		households_for_settlement = np.empty(self.__starting_households, dtype = Household)
		for i in range(self.__starting_households):
			c_id = self.c_id+1
			h = Household(c_id, self.__starting_household_size,self.__starting_grain,self.__min_competency, self.__min_ambition, self.__rental_rate, self.__allow_land_rental, self.__distance_cost,self.__knowledge_radius)
			self.__household_List[i] = h
			households_for_settlement[i] = h

		return households_for_settlement
		#creates and returns a list of households for the belonging settlement

	'''Calls the create river method in map'''
	def createRiver(self):
		#sets the first 2 columns of the Map to river
		#this means setting the Patch objects' attribute isRiver to true
		#and chanding the colour of the 2 columns to blue
		#this method will be called within the run simulation method
		self.map.createRiver()

	'''Calculates the total population based on user input'''
	def establishPopulation(self):
		self.__total_population = self.__starting_settlements * self.__starting_households * self.__starting_household_size

	'''Allows for population maintenance as households 'die', simulating a movement of workers from failed households to more successful households
	 as well as more natural population increase (higher birth-rate vs death-rate)
	 but to keep the overall population density and growth to within reasonable limits that correlate with those projected by historians and archaeologists,
	 who reconstruct a less than .1% annual population growth for Egypt in the predynastic period.
	 One might expect greater growth here than the average for all of Egypt, which is why there is a slide that lets the user play around with this and see how it affects the model.'''
	def populationShift(self, household, settlement, ticks):
		starting_pop =  self.__starting_settlements * self.__starting_households * self.__starting_household_size
		populate_chance = random.uniform(0,1) #creates a random float between 0 and 1
		if(self.__total_population <= (starting_pop * math.pow((1 + (self.__pop_growth_rate/100)),ticks)) and (populate_chance > 0.5)):
			household.addMember()
			settlement.incrementPopulation()
			self.__total_population += 1
			#if criteria is met (based on population, population growth rate, ticks and an arbritrary population chance), household will gain a new worker
		self.__projected_historical_population = math.pow((starting_pop * 1.001),ticks)

	'''Sets the respective class variables to the input entered by the user'''
	def saveUserInput(self, time, settlements, households, household_size, grain, comp, amb, gen_var,
		knowledge, dist, fallow, pop_growth, allow_rent, rent_rate):
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
		self.__allow_land_rental = allow_rent
		self.__rental_rate = rent_rate
		#captured upon clicking the setup button

		#the below methods are then called to run (after setup is clicked)
		self.setUpPatches()
		self.setUpSettlements()
		self.createRiver()
		self.establishPopulation()
		self.runSimulation()


	def change_state(self):
		if self.continuePlotting == True:
			self.continuePlotting = False
		else:
			self.continuePlotting = True

	'''plots a graph on a additional figure window'''
	def populationGraph(self):
		#print("IN POP GR")
		self.x.append(self.count)
		self.y.append(self.__total_population)
		self.ax2.plot(self.x,self.y, 'b')
		self.fig2.canvas.draw()
		self.fig2.canvas.flush_events()
		self.after(0, self.getData())

	def change_stateGraph(self):
		if self.graphPlotting == True:
			self.graphPlotting = False
		else:
			self.graphPlotting = True

	def runSimulation(self):
		cmap = mpl.colors.ListedColormap(['blue', '#00ff00','#00ed00','#00e600','#00df00','#00da00','#00d400','#00ce00','#00c400','#00bc00','#00b300','#00aa00','#00a500','#009e00','#009900','#007e00'])

		self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")

		self.cv = FigureCanvasTkAgg(self.fig, master=root)
		self.cv.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

		for i in self.coordinates:
			self.ax.plot(i[1],i[0], marker='$⌂$', ms = '11')

		#self.fig2.show()
		#self.change_state()
		#thread1 = threading.Thread(target=self.getData())
		# **********************************
		# 		    GRAPH WINDOW
		# **********************************
		#thread1.start()
		self.getData()
		#self.change_stateGraph()
		#thread2 = threading.Thread(target=self.populationGraph)
		#thread2.start()
		# **********************************

		root.geometry("1200x700")

		self.ax.axis('off')

	'''get Data is the fundamental method of the simulation. It goes through the entire model time span year by year. This method traverses
	through the settlement list (including all settlement objects), and its household list (including all household objects belonging to that
	settlement), every year, year by year. Inside these two for loops, all the main functions of the simulation are called'''
	def getData(self):
		self.xList =[] #list of x coordinates of fields claimed
		self.yList = [] #list of x coordinates of fields claimed
		root.geometry("1200x700")
		self.ax.axis('off')
		#tick_Counter = tk.Label (root, text = ("Ticks:", 0))

		#tick_Counter.pack()
		cmap = mpl.colors.ListedColormap(['blue', '#00ff00','#00ed00','#00e600','#00df00','#00da00','#00d400','#00ce00','#00c400','#00bc00','#00b300','#00aa00','#00a500','#009e00','#009900','#007e00'])
		#A list of colours associated with the values in the grid
		count = 0
		while(self.count<self.__model_time_span): #Goes through the model time span

			self.count += 1

			self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")
			#shows the grid and plots the colours of the associated grid values to the position in the cmap array

			#tick_Counter['text'] = ('Ticks:', count)
			for s in self.__settlement_List: #traverses through settlement list
				self.ax.plot(s.getCoordinates()[1],s.getCoordinates()[0], marker='$⌂$', ms = str(s.checkSettlementPopulation()), color = 'yellow')
				self.ax.plot(s.getCoordinates()[1], s.getCoordinates()[0], marker = 's' ,markerfacecolor = 'yellow',markeredgecolor='yellow', ms = 6.5)
				#plots the settlements in the shape of a house in the position of its coordinates

				for h in s.getHouseholdList(): #traverses through the households in the settlement

					self.map.flood() #calls the flood method in Map

					h.setCoordinates(s.getCoordinates()) #sets the coordinates in household (same as its settlement)
					x = h.claimFields(s.getCoordinates()[0],s.getCoordinates()[1])
					#claim field method is called which returns the coordinates of the field claimed (assigned to the variable x)

					self.populationShift(h, s, count) #population shift method called

					h.generationalChangeover(self.__generation_variation,self.__min_ambition, self.__min_competency)
					#generational changeover method called

					num_harvests = math.floor(h.getSize() / 2) #one harvest for every 2 workers
					for i in range(num_harvests):
						farm = h.inner.beginFarm()
						if(farm):
							self.ax.plot(farm[0], farm[1], marker = '$☘$' ,markerfacecolor = 'g',markeredgecolor='white' ,ms = 10, color = 'g')
					#farm method called which returns the coordinates of the the field to be harvested and displays a clover at the position of the field

					for field in h.getFieldsOwned():
						if(field.inner.fieldChangeover() >= self.__fallow_limit):
							field.toggleOwned()
							h.removeField(field)
							self.ax.lines.remove(self.ax.lines[0])
					#calls field changeover method in Field on each of the fields owned by the household

					if(h.consumeGrain()):
						s.decrementPopulation()
						self.__total_population =- 1
					#consume grain method called which returns a boolean value. If true, a member is lost and population is decreased

					if(h.checkWorkers()):
						s.removeHousehold(h)
					#check workers method called which returns a boolean value. If true, a household is removed from the settlement

					h.storageLoss()
					#storage method lost method is called

					try:
						self.xList.append(x[0])
						self.xList.append(s.getCoordinates()[1])
						self.yList.append(x[1])
						self.yList.append(s.getCoordinates()[0])
						#appends the coordinates of the fields claimed to these respective x and y arrays

						self.ax.plot(self.xList, self.yList, marker = '.' ,markerfacecolor = 'g',markeredgecolor='g',color = 'white', ms = 6, linestyle='-')
						self.ax.plot(s.getCoordinates()[1], s.getCoordinates()[0], marker = 's' ,markerfacecolor = 'yellow',markeredgecolor='yellow', ms = 6.5)
						#fields claimed are plotted with a dot and a connecting line from the settlement
						self.cv.draw()
						self.cv.flush_events()

						#time.sleep(0.01)
						self.xList.clear()
						self.yList.clear()
						#self.after(0, self.populationGraph())

					except:
						continue

			if(self.__allow_land_rental):
				for s in self.__settlement_List:
					for h in s.getHouseholdList():
						num = h.getSize() - h.inner.getWorkersWorked() #workers who didn't previously farm this year
						for i in range(num):
							h.rentLand()
			#settlements and households are traversed through again because rent land can only be called after all main farming/harvesting is completed
			#rent land is then called (if user selected allow land rental) on each household (for each worker who didn't previously farm this year)


			for line in self.ax.lines:
				line.set_marker(".")

			#removes the clover each year and changes to a dot (claim field) to show that fields become unharvested every year

if __name__ == "__main__":
	root=tk.Tk()
	root.title("Egypt Simulation")
	root.geometry("480x700")
	Simulate(root).pack(side=tk.LEFT, fill="both", expand=True)
	root.mainloop()
