
##
## CS 4222/5222 Artificial Intelligence
## Spring 2020
##
## Lab 2: path finding
##
##

import math
import pickle
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from time import time, sleep
from pathlab import *


## spherical Mercator projection of lat/lon coords
def merc(coords,mapw,maph):
    x = (coords[1]+180)*(mapw/360.0)
    latRad = coords[0]*math.pi/180.0
    mercN = math.log(math.tan((math.pi/4.0)+(latRad/2.0)))
    y = maph/2.0 - (maph*mercN)/(2.0*math.pi)
    return (x,y)

## transform coordinates from graph locations to fit on canvas
## margin is pixels of padding from canvas bounding box
def transform(coords,graph,canvas):
    margin=50    
    wfactor = canvas.winfo_reqwidth() - 2*margin
    hfactor = canvas.winfo_reqheight() - 2*margin

    if graph.geo:
        maxproj = merc((graph.xmax,graph.ymax),wfactor,hfactor)
        minproj = merc((graph.xmin,graph.ymin),wfactor,hfactor)
        x,y = merc(coords,wfactor,hfactor)
        rx = wfactor/(maxproj[0]-minproj[0])
        ry = hfactor/(maxproj[1]-minproj[1])
        return (rx*(x-minproj[0])+margin,hfactor-ry*(y-minproj[1])+margin)
    else:
        x,y = coords
        rx = wfactor/(graph.xmax-graph.xmin)
        ry = hfactor/(graph.ymax-graph.ymin)    
        return (rx*(x-graph.xmin)+margin,hfactor-ry*(y-graph.ymin)+margin)

    
## Draw the graph on the main canvas
def draw(graph):
    for v in graph.nodes():
        x1,y1 = transform(graph.locations[v],graph,canvas)
        for u in graph.dict[v]:
            x2,y2 = transform(graph.locations[u],graph,canvas)
            canvas.create_line(x1,y1,x2,y2)
    for node in graph.locations:
        x,y = transform(graph.locations[node],graph,canvas)
        canvas.create_rectangle( x-1, y-1, x+1, y+1, fill = "gray" )
        if len(graph.nodes()) < 50: canvas.create_text(x-2,y-2,text=node)

## Trace the path (list of nodes) in red on the canvas
def draw_path(graph,path):
    coords = list(map(lambda v: transform(graph.locations[v.state],graph,canvas),path))
    x,y = coords[0]
    canvas.create_rectangle( x-3, y-3, x+3, y+3, fill = "red" )
    for xnext,ynext in coords[1:]:
        canvas.create_line(x,y,xnext,ynext,width=4,fill="red")
        x,y = xnext,ynext

## Retrieve the solution from the path, calculate its cost and display
def get_solution(graph,path):
    cost=0;
    statePath = list(map(lambda v: v.state,path))
    statePath.reverse()
    for i in range(len(statePath)-1):
        cost = cost+graph.get(statePath[i],statePath[i+1])
    pathCostStr.set(str(cost))

## Mark all the nodes in the fringe set with blue
def draw_fringe(graph,fringe):
    coords = map(lambda v: graph.locations[v.state],fringe)
    for x,y in coords:
        x,y = transform((x,y),graph,canvas)
        canvas.create_rectangle( x-3, y-3, x+3, y+3, fill = "blue" )

## Mark all the nodes in the closed set with black
def draw_closed(graph,closed):
    coords = list(map(lambda state: transform(graph.locations[state],graph,canvas),closed))
    for x,y in coords:
        canvas.create_rectangle( x-3, y-3, x+3, y+3, fill = "black" )

## Display the number of nodes generated since search began
def display_nodecount():
    nodeCountStr.set(str(Node.nodecount))

## Callback registered with search algorithm to be called in each
## iteration to display the search state
def callback(graph,node,fringe,closed,halt):
    canvas.delete("all")
    draw(graph)
    draw_fringe(graph,fringe)
    draw_path(graph,node.path())
    draw_closed(graph,closed)
    display_nodecount()
    if halt: get_solution(graph,node.path())
    root.update_idletasks()
    sleep(speed.get())

## Create a search problem on the graph, with initial state and goal,
## and run the selected search algorithm
def run(graph):
    speedLabel['state']=DISABLED
    speedSlider['state'] = DISABLED
    prob = SearchProblem(start.get(),goal.get(),graph)
    pathCostStr.set("")
    if algo.get() == "graph search":
        graph_search(prob,[],callback)
    elif algo.get() == "BFS":
        breadth_first_graph_search(prob,callback)
    elif algo.get() == "DFS":
        depth_first_graph_search(prob,callback)
    elif algo.get() == "greedy best-first":
        best_first_graph_search(prob, prob.h, callback)
    elif algo.get() == "A*":
        astar_search(prob, callback)
    elif algo.get() == "IDS":
        iterative_deepening_search(prob, callback)
    else:
        showerror(message="Unknown algorithm selected")
    speedLabel['state'] = NORMAL
    speedSlider['state'] = NORMAL

def loadInstance():
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    with open(filename,'rb') as f: graph= pickle.load(f)
    f.close()

    ## compute bounding box corners
    graph.xmin = min([x for (x,y) in graph.locations.values()])
    graph.xmax = max([x for (x,y) in graph.locations.values()])
    graph.ymin = min([y for (x,y) in graph.locations.values()])
    graph.ymax = max([y for (x,y) in graph.locations.values()])

    ## Populate menus
    startNodeMenu['menu'].delete(0,'end')
    startNodeMenu['state']=NORMAL
    startNodeLabel['state']=NORMAL
    for node in graph.nodes():
        startNodeMenu['menu'].add_command(label=node, command=lambda x=node:start.set(x))
    start.set(graph.default_start)
    goalNodeMenu['menu'].delete(0,'end')
    goalNodeMenu['state']=NORMAL
    goalNodeLabel['state']=NORMAL
    for node in graph.nodes():
        goalNodeMenu['menu'].add_command(label=node, command=lambda x=node:goal.set(x))
    goal.set(graph.default_goal)
    canvas.delete("all")
    draw(graph)
    go.configure(command=lambda x=graph:run(graph))
    go['state'] = NORMAL

## Initialize environment
root = Tk()
windowWidth = 1200
windowHeight = 700
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("{}x{}".format(windowWidth, windowHeight) + "+{}+{}".format(positionRight, positionDown))
root.title( "Search Animator" )

## Set up canvas for input window
canvas = Canvas( root, width=windowWidth-300, height=windowHeight )
canvas.place(x=0,y=0)

## Set up canvas for control panel
controlFrame = Frame(root, height=windowHeight-180,width=275,borderwidth=2,relief=SUNKEN)
controlFrame.place(x=900,y=200/2);
controlFrame.propagate(0)
control = Canvas(controlFrame)
control.pack(expand=YES,fill=BOTH)


## Start node menu (this needs to be populated after load)
start = StringVar(root)
startNodeMenu = OptionMenu(control,start,None)
startNodeMenu.grid(row=2,column=2,sticky=W,padx=5,pady=5)
startNodeLabel = Label(control,text="Start:")
startNodeLabel.grid(row=2,column=1,sticky=E,padx=5,pady=5)
startNodeMenu["state"]=DISABLED
startNodeLabel["state"]=DISABLED

## Goal node menu (this needs to be populated after load)
goal = StringVar(root)
goalNodeMenu = OptionMenu(control,goal,None)
goalNodeMenu.grid(row=3,column=2,sticky=W,padx=5,pady=5)
goalNodeLabel = Label(control,text="Goal:")
goalNodeLabel.grid(row=3,column=1,sticky=E,padx=5,pady=5)
goalNodeMenu["state"]=DISABLED
goalNodeLabel["state"]=DISABLED

## Algo menu
algos = ["graph search", "BFS", "DFS", "greedy best-first", "A*", "IDS"]
algo = StringVar(root)
algo.set(algos[0])
algoMenu = OptionMenu(control,algo,*algos)
algoMenu.grid(row=4,column=2,sticky=W,padx=5,pady=5)
Label(control,text="Algo:").grid(row=4,column=1,sticky=E,padx=5,pady=5)

graph=None

## Go button
go = Button(control,text="Go",width=10)
go.grid(row=1,column=1,sticky='w',padx=5,pady=5)
go["state"] = DISABLED
go.propagate(0)

## Load button
load = Button(control,text='Load',width=10,command=loadInstance)
load.grid(row=1,column=2,sticky='w',padx=5,pady=5)
load.propagate(0)

## Nodes generated display
nodeCountStr = StringVar(root)
Label(control,text="Nodes generated:").grid(row=5,column=1,sticky=E,padx=5,pady=5)
Label(control,textvariable=nodeCountStr).grid(row=5,column=2,sticky=W,padx=5,pady=5)
nodeCountStr.set("0")

## Solution cost display
pathCostStr = StringVar(root)
Label(control,text="Solution cost:").grid(row=6,column=1,sticky=E,padx=5,pady=5)
Label(control,textvariable=pathCostStr).grid(row=6,column=2,sticky=W,padx=5,pady=5)
pathCostStr.set("")

speed = DoubleVar(root)
speedLabel  = Label(control,text="Speed:")
speedSlider = Scale(control,from_=1,to=0.01,resolution=0.01,variable=speed,orient=HORIZONTAL,
                    showvalue=False)
speed.set(1)
speedLabel.grid(row=7,column=1,sticky=E,padx=5,pady=5)
speedLabel.propagate(0)
speedSlider.grid(row=7,column=2,sticky=W,padx=5,pady=5)
speedSlider.propagate(0)


## Main loop
if __name__ == "__main__":
    root.mainloop()

