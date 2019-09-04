import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import matplotlib.patches as ptc
from matplotlib.patches import Circle
import matplotlib.image as mpimg
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
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
from Map import Map
from Settlement import Settlement
from Household import Household
from Patch import Patch
from Flood import Flood
import math
plt.style.use('ggplot')

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
	fig = plt.figure(figsize=(10,8.2))
	ax = fig.add_subplot(1,1,1)
	#totPop = plt.subplot2grid((6,2), (0,0), rowspan = 2 , colspan= 1)
	xList = []
	yList = []
	global c_id
	__model_time_span = 0
	__manual_seed = False
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
	__total_population = 0
	__household_List= np.empty(250, dtype= Household) #List of all Household objects
	__settlement_List = []
	coordinates = []
	cv = fig
	#x, y = np.empty(20, dtype= int)
	#__grid = np.random.randint(10, size= (40,40))
	map = Map()
	flood = Flood()



	def __init__(self, root):

		tk.Frame.__init__(self, root)
		self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
		# **********************************
		# 			User Inputs
		# **********************************
		mtp = tk.Scale(self.scrollFrame.viewPort, from_=100, to=500, orient=HORIZONTAL, label = "Model Time Span:", length = 180, resolution=50)
		mtp.pack(padx=20, pady=10, side=tk.TOP)
		mtp.set(100)

		varSeed = IntVar()
		chkSeed = tk.Checkbutton (self.scrollFrame.viewPort, text = "Manual Seed" , padx = 0, pady = 2, variable = varSeed)
		chkSeed.pack()

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

		varFis = IntVar()
		chkFis = tk.Checkbutton (self.scrollFrame.viewPort, text = "Household Fission" , padx = 0, pady = 2, variable= varFis)
		chkFis.pack()

		mfc = tk.Scale(self.scrollFrame.viewPort, from_=0, to=10, orient=HORIZONTAL, label = "Min Fission Chance:", length = 180)
		mfc.pack()
		mfc.set(4)

		varRent = IntVar()
		chkRent = tk.Checkbutton (self.scrollFrame.viewPort, text = "Land Rental" , padx = 0, pady = 2, variable = varRent)
		chkRent.pack()

		rr = tk.Scale(self.scrollFrame.viewPort, from_=0, to=10, orient=HORIZONTAL, label = "Rental Rate %:", length = 180)
		rr.pack()
		rr.set(5)
		# **********************************
		# Now add some controls to the scrollframe.
		# NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
		self.scrollFrame.pack(side=tk.LEFT, fill="both", expand=True)
		# when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)

		'''
		def on_key_press(event):
			print("you pressed {}".format(event.key))
			key_press_handler(event, cv, toolbar)
		cv.mpl_connect("key_press_event", on_key_press)
		'''
		def _quit():
			root.quit()     # stops mainloop
			root.destroy()

		def createPlots():
			xs = []
			ys = []
			for i in range(10):
				x = i
				y = random.randrange(10)
				xs.append(x)
				ys.append(y)
			return xs, ys

		def _start():

			# **********************************
			# 		    GRAPH WINDOW
			# **********************************
			graphWindow = Toplevel()
			self.gw = ScrollFrame(graphWindow)
			graphWindow.title("Graphs")
			x, y = createPlots()

			#self.totPop.plot(x, y)

			self.gw.pack(fill="both", expand=True, anchor = "e")
			graphWindow.geometry("600x700")
			# **********************************

			rent = False
			seed = False
			fis = False

			if(varRent == 1):
				rent = True

			if(varSeed == 1):
				seed = True

			if(varFis == 1):
				fis = True

			self.saveUserInput(mtp.get(), ss.get(), sh.get(), shs.get(), sg.get(), mc.get(), \
			ma.get(), gv.get(), kr.get(), dc.get(), fl.get(), pg.get(),fis, \
			mfc.get(), rent, rr.get(), seed)

		def _stop():
			root.quit()     # stops mainloop
			root.destroy()

		# **********************************
		# 		 INFORMATION WINDOW
		# **********************************
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
			p3 = tk.Label(self.sf.viewPort, text = "\n(how to use the model, including a description of each of the items in the Interface tab)\n", font = "calibri", fg = "black", bd = 10, width = 60, justify = LEFT)
			p3.pack()

			h4 = tk.Label(self.sf.viewPort, text = "THINGS TO NOTICE", bg= "lightblue", font = "calibri", fg = "black", bd = 10, width = 60)
			h4.pack()
			p4 = tk.Label(self.sf.viewPort, text = "\n(suggested things for the user to notice while running the model)\n", font = "calibri", fg = "black", bd = 10, width = 60, justify = LEFT)
			p4.pack()

			h5 = tk.Label(self.sf.viewPort, text = "THINGS TO TRY", bg= "lightblue", font = "calibri", fg = "black", bd = 10, width = 60)
			h5.pack()
			p6 = tk.Label(self.sf.viewPort, text = "\n(suggested things for the user to try to do (move sliders, switches, etc.) with the model)\n", font = "calibri", fg = "black", bd = 10, width = 60, justify = LEFT)
			p6.pack()

			self.sf.pack(fill="both", expand=True)
			informationWindow.geometry("600x700")
		# **********************************

		start = tk.Button(master=root, text="Start", command=_start)
		start.pack(in_ = self.scrollFrame, side=tk.LEFT)

		stop = tk.Button(master=root, text="Stop", command=_stop)
		stop.pack(in_ = self.scrollFrame, side=tk.LEFT)

		quit = tk.Button(master=root, text="Quit", command=_quit)
		quit.pack(in_ = self.scrollFrame, side=tk.LEFT)

		info = tk.Button(master=root, text="Info", command=_info)
		info.pack(in_ = root, side=tk.TOP)

		self.scrollFrame.pack(side="top", fill="both", expand=True)
		#self.img=mpimg.imread('/Users/user/Desktop/CSC3003S/EGYPT/Egypt_Simulation/map.png') #image is imported into a numpy array which will be used for the flooding simulation each tick


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
			h = Household(c_id, settle.getCoordinates(), self.__starting_household_size, self.__min_competency, self.__min_ambition, self.__knowledge_radius)
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
		self.__total_population = self.__starting_settlements * self.__starting_households * self.__starting_household_size

	def populationShift(self, household, settlement, ticks):
		starting_pop =  self.__starting_settlements * self.__starting_households * self.__starting_household_size
		populate_chance = random.uniform(0,1) #creates a random float between 0 and 1
		if(self.__total_population <= (starting_pop * math.pow((1 + (self.__pop_growth_rate/10000)),ticks)) and (populate_chance > 0.5)):
			household.addMember()
			settlement.incrementPopulation()
			self.__total_population += 1
		self.__projected_historical_population = math.pow((starting_pop * 1.001),ticks)

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

	def calcTotalPopulation():
		return self.__starting_settlements * self.__starting_households * self.__starting_household_size

	def saveUserInput(self, time, settlements, households, household_size, grain, comp, amb, gen_var,
		knowledge, dist, fallow, pop_growth, allow_fission, fission_chance, allow_rent, rent_rate, manual_seed):
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
		self.__manual_seed = manual_seed

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


	def runSimulation(self):
		cmap = mpl.colors.ListedColormap(['blue', '#00ff00','#00ed00','#00e600','#00df00','#00da00','#00d400','#00ce00','#00c400','#00bc00','#00b300','#00aa00','#00a500','#009e00','#009900','#007e00'])

		self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")

		#self.getData()
		#self.ax.imshow(self.img)
		self.cv = FigureCanvasTkAgg(self.fig, master=root)
		self.cv.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

		for i in self.coordinates:
			self.ax.plot(i[1],i[0], marker='$⌂$', ms = '11')

		self.change_state()
		threading.Thread(target=self.getData()).start()

		root.geometry("1200x700")

		self.ax.axis('off')

	def getData(self):
		self.xList =[]
		self.yList = []
		print("IN GET CO")
		root.geometry("1200x700")
		self.ax.axis('off')
		#tick_Counter = tk.Label (root, text = ("Ticks:", 0))

		#tick_Counter.pack()
		cmap = mpl.colors.ListedColormap(['blue', '#00ff00','#00ed00','#00e600','#00df00','#00da00','#00d400','#00ce00','#00c400','#00bc00','#00b300','#00aa00','#00a500','#009e00','#009900','#007e00'])

		count = 0
		while(count<self.__model_time_span):

			count += 1
			flood = Flood()

			self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")
			#**********Check every tick that allows for information to be used for the graphs to keep them updated***********
			self.establishPopulation() # dont think this is the right method - we need a method that checks the population every tick
			#****************************************************************************************************************

			#tick_Counter['text'] = ('Ticks:', count)
			for s in self.__settlement_List:
				for h in s.getHouseholdList():
					flood.setFertility()

					h.setCoordinates(s.getCoordinates())
					x = h.claimFields(s.getCoordinates()[0],s.getCoordinates()[1])

					self.populationShift(h, s, count)

					h.generationalChangeover(self.__generation_variation,self.__min_ambition, self.__min_competency)

					num_harvests = math.floor(h.getSize() / 2) #one harvest for every 2 workers
					for i in range(num_harvests):
						h.inner.beginFarm(self.__distance_cost)

					for field in h.getFieldsOwned():
						if(field.inner.fieldChangeover() >= self.__fallow_limit):
							field.toggleOwned()
							h.removeField(field)

					if(h.consumeGrain()):
						s.decrementPopulation()
						self.__total_population =- 1

					if(h.checkWorkers()):
						s.removeHousehold(h)

					try:
						self.xList.append(x[0])
						self.xList.append(s.getCoordinates()[1])
						self.yList.append(x[1])
						self.yList.append(s.getCoordinates()[0])

						self.ax.plot(self.xList, self.yList, marker = '$☘$', markeredgecolor = 'green' ,color = 'white', ms = 8, linestyle='-')
						self.cv.draw()
						self.cv.flush_events()

						#time.sleep(0.01)
						self.xList.clear()
						self.yList.clear()

					except:
						continue

if __name__ == "__main__":
	root=tk.Tk()
	root.title("Egypt Simulation")
	root.geometry("480x700")
	Simulate(root).pack(side=tk.LEFT, fill="both", expand=True)
	root.mainloop()
