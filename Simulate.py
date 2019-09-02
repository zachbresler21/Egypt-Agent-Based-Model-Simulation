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
import random
from Map import Map
from Settlement import Settlement
from Household import Household
from Patch import Patch
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

	fig = plt.figure(figsize=(10,8.2))
	ax = fig.add_subplot(1,1,1)
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
	#x, y = np.empty(20, dtype= int)
	#__grid = np.random.randint(10, size= (40,40))
	map = Map()

	def __init__(self, root):

		tk.Frame.__init__(self, root)
		self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
		# **********************************
		# 			User Inputs
		# **********************************
		mtp = tk.Scale(self.scrollFrame.viewPort, from_=100, to=500, orient=HORIZONTAL, label = "Model Time Span:", length = 180, resolution=50, cursor = "hand")
		mtp.pack(padx=20, pady=10, side=tk.TOP)
		mtp.set(100)

		varSeed = IntVar()
		chkSeed = tk.Checkbutton (self.scrollFrame.viewPort, text = "Manual Seed" , padx = 0, pady = 2, variable = varSeed)
		chkSeed.pack()

		ss = tk.Scale(self.scrollFrame.viewPort, from_=5, to=20, orient=HORIZONTAL, label = "Starting Settlements:", length = 180, cursor = "hand")
		ss.pack(pady = 10)
		ss.set(5)

		sh = tk.Scale(self.scrollFrame.viewPort, from_=1, to=10, orient=HORIZONTAL, label = "Starting Households:", length = 180, cursor = "hand")
		sh.pack()
		sh.set(3)

		shs = tk.Scale(self.scrollFrame.viewPort, from_=1, to=10, orient=HORIZONTAL, label = "Starting Household Size:", length = 180, cursor = "hand")
		shs.pack()
		shs.set(3)

		sg = tk.Scale(self.scrollFrame.viewPort, from_=100, to=8000, orient=HORIZONTAL, label = "Starting Grain:", length = 180, cursor = "hand")
		sg.pack()
		sg.set(3500)

		ma = tk.Scale(self.scrollFrame.viewPort, from_=0.0, to=1.0, orient=HORIZONTAL, label = "Min Ambition:", length = 180, resolution=0.1, cursor = "hand")
		ma.pack()
		ma.set(0.4)

		mc = tk.Scale(self.scrollFrame.viewPort, from_=0.0, to=1.0, orient=HORIZONTAL, label = "Min Competency:", length = 180, resolution=0.1, cursor = "hand")
		mc.pack()
		mc.set(0.5)

		gv = tk.Scale(self.scrollFrame.viewPort, from_=0.0, to=1.0, orient=HORIZONTAL, label = "Generation Variation:", length = 180, resolution=0.1, cursor = "hand")
		gv.pack()
		gv.set(0.2)

		kr = tk.Scale(self.scrollFrame.viewPort, from_=5, to=40, orient=HORIZONTAL, label = "Knowledge Radius:", length = 180, cursor = "hand")
		kr.pack()
		kr.set(15)

		dc = tk.Scale(self.scrollFrame.viewPort, from_=1, to=15, orient=HORIZONTAL, label = "Distance Cost (kg):", length = 180, cursor = "hand")
		dc.pack()
		sh.set(3)

		fl = tk.Scale(self.scrollFrame.viewPort, from_=0, to=50, orient=HORIZONTAL, label = "Fallow Limit:", length = 180, cursor = "hand")
		fl.pack()
		fl.set(17)

		pg = tk.Scale(self.scrollFrame.viewPort, from_=0, to=50, orient=HORIZONTAL, label = "Population Growth %:", length = 180, cursor = "hand")
		pg.pack()
		pg.set(20)

		varFis = IntVar()
		chkFis = tk.Checkbutton (self.scrollFrame.viewPort, text = "Household Fission" , padx = 0, pady = 2, variable= varFis)
		chkFis.pack()

		mfc = tk.Scale(self.scrollFrame.viewPort, from_=0, to=10, orient=HORIZONTAL, label = "Min Fission Chance:", length = 180, cursor = "hand")
		mfc.pack()
		mfc.set(4)

		varRent = IntVar()
		chkRent = tk.Checkbutton (self.scrollFrame.viewPort, text = "Land Rental" , padx = 0, pady = 2, variable = varRent)
		chkRent.pack()

		rr = tk.Scale(self.scrollFrame.viewPort, from_=0, to=10, orient=HORIZONTAL, label = "Rental Rate %:", length = 180, cursor = "hand")
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
			root.destroy()  # this is necessary on Windows to prevent
							# Fatal Python Error: PyEval_RestoreThread: NULL tstate
		def _start():
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

		def _pause():
			root.quit()     # stops mainloop
			root.destroy()

		def _stop():
			root.quit()     # stops mainloop
			root.destroy()

		start = tk.Button(master=root, text="Start", command=_start, cursor = "pointinghand")
		start.pack(in_ = self.scrollFrame, side=tk.LEFT)

		pause = tk.Button(master=root, text="Pause", command=_pause, cursor = "pointinghand")
		pause.pack(in_ = self.scrollFrame, side=tk.LEFT)

		stop = tk.Button(master=root, text="Stop", command=_stop, cursor = "pointinghand")
		stop.pack(in_ = self.scrollFrame, side=tk.LEFT)

		quit = tk.Button(master=root, text="Quit", command=_quit, cursor = "pointinghand")
		quit.pack(in_ = self.scrollFrame, side=tk.LEFT)

		self.scrollFrame.pack(side="top", fill="both", expand=True)
		self.img=mpimg.imread('/Users/user/Desktop/CSC3003S/EGYPT/Egypt_Simulation/map.png')
		

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
		if(self.__total_population <= (starting_pop * math.pow((1 + (self.__pop_growth_rate/100)),ticks)) and (populate_chance > 0.5)):
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

	def runSimulation(self):
		cmap = mpl.colors.ListedColormap(['blue', 'lightgreen'])

		self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")
		
		

		self.getData()

		self.cv = FigureCanvasTkAgg(self.fig, master=root)
		self.cv.draw()
		self.cv.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
		for i in self.coordinates:
			self.ax.plot(i[1],i[0], marker='$⌂$', ms = '11')
		'''
		for i in range(self.__model_time_span):
			#ani = animation.FuncAnimation(self.fig, self.animate(1000), interval=1000)
			self.animate(i)
			#self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")
		'''
		root.geometry("1200x700")
		
		self.ax.axis('off')

	def getData(self):
		self.xList =[]
		self.yList = []
		print("IN GET CO")
		
		
		#tick_Counter = tk.Label (self.scrollFrame.viewPort, text = ("Ticks:", 0)) 
		#tick_Counter.pack(side = tk.TOP)
		
		count =0
		while(count<self.__model_time_span):

			count += 1
			#tick_Counter['text'] = ('Ticks:', count)
			for s in self.__settlement_List:
				for h in s.getHouseholdList():
					x = h.claimFields(s.getCoordinates()[0],s.getCoordinates()[1])
					try:
						self.xList.append(x[0])
						self.xList.append(s.getCoordinates()[0])
						
						self.yList.append(x[1])
						self.yList.append(s.getCoordinates()[1])
					except:
						continue 
				self.ax.plot(self.yList, self.xList, marker = '$☘$',markeredgecolor = 'green' ,color = 'white', ms = 8, linestyle='-')
				self.xList.clear()
				self.yList.clear()
				
	'''
	def animate(self, x):
		#self.getData()
		self.ax.clear()
		
		#cmap = mpl.colors.ListedColormap(['blue','lightgreen'])
		#self.ax.imshow(self.map.getGrid(),vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation= "None")
		self.ax.imshow(self.img)

		self.ax.plot(self.yList, self.xList, marker = '$☘$', color = 'white', ms = 8, linestyle='-')
		
		for i in self.coordinates:
			self.ax.plot(i[1],i[0], marker='$⌂$', ms = '11')
	'''
if __name__ == "__main__":
	root=tk.Tk()
	root.title("Egypt Simulation")
	root.geometry("480x700")
	Simulate(root).pack(side=tk.LEFT, fill="both", expand=True)
	root.mainloop()

