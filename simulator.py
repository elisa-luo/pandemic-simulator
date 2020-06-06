import random
import math
from matplotlib import pyplot as plt
import numpy as np
plt.rcParams['figure.dpi'] = 75

def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    
recovery_time = 10 # recovery time in time-steps
virality = 0.5    # probability that a neighbor cell is infected in 
                  # each time step                                                  

class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y 
        self.state = "S" # can be "S" (susceptible), "R" (resistant = dead), or 
                         # "I" (infected)
        self.time = 0
    
    def __str__(self):
        return str(self.x) + ', ' + str(self.y)
    
    def infect(self):
        self.time = 0
        self.state = "I"
        
    def recover(self):
        self.state = "S"
        self.time =0
        #print("i recovered")
    
    def process(self, adjacent_cells):
        if self.state != "I" or self.time<=1:
            self.time+=1
            return
        if self.state == "I" and self.time>=recovery_time:
            self.recover()
            return
        rand1 = random.random()
        if self.state == "I" and rand1<=pdeath(self.time, 10,2):
            self.state = "R" #cell has died
            #print("i died")
            self.time =0
            return
        if self.state == "I":
            for adj in adjacent_cells:
                if adj.state == "S": #can be infected
                    rand  = random.random()
                    if rand <= virality:
                        adj.infect()
            self.time+=1
                
 
        
class Map(object):
    
    cells = dict()
    
    def __init__(self):
        self.height = 150
        self.width = 150           
        self.cells = {}

    def add_cell(self, cell):
        self.cell = cell
        key = (cell.x, cell.y)
        self.cells[key] = self.cell
        
    def display(self):
        img = np.zeros((150,150,3), dtype = np.uint8)
        for key in self.cells:
            cell = self.cells[key]
            if cell.state == "S":
                img[cell.x, cell.y,0] = 0
                img[cell.x, cell.y,1] = 255 #green
                img[cell.x, cell.y,2] = 0
            elif cell.state == "R":
                img[cell.x, cell.y,0] = 130 #grey
                img[cell.x, cell.y,1] = 130
                img[cell.x, cell.y,2] = 130
            elif cell.state == "I":
                img[cell.x, cell.y,0] = 255 #red
                img[cell.x, cell.y,1] = 0
                img[cell.x, cell.y,2] = 0
        plt.imshow(img) 
    
    def adjacent_cells(self, x,y):
        #returns a list of cell instances adjacent to the coordinates x,y
        li_cells = []
        if (x+1,y) in self.cells:
            li_cells.append(self.cells[(x+1,y)])
        if (x-1,y) in self.cells:
            li_cells.append(self.cells[(x-1,y)])
        if (x,y+1) in self.cells:
            li_cells.append(self.cells[(x,y+1)])
        if (x,y-1) in self.cells:
            li_cells.append(self.cells[(x,y-1)])
        
        return li_cells
    
    def time_step(self):
        # Update each cell on the map 
        # display the map.
        for key in self.cells:
            temp_cell = self.cells[key]
            x = key[0]
            y= key [1]
            temp_cell.process(self.adjacent_cells(x,y))
        self.display()
        
        # ... cell.process(adjacent_cells... )
       

            
def read_map(filename):
    
    m = Map()
    
    f = open(filename,'r')
    
    for line in f:
        coordinates = line.strip().split(',')
        c = Cell(int(coordinates[0]),int(coordinates[1]))
        Map.add_cell(m, c)

    return m
