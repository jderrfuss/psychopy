from psychopy import visual, event, core
"""ShapeStim can be used to make geometric shapes where you specify the locations of each vertex
relative to some anchor point. 

NB for now the fill of objects is performed using glBegin(GL_POLYGON) and that is limited to convex 
shapes. With concavities you get unpredictable results (e.g. add a fill colour to the arrow stim below). 
To create concavities, you can combine multiple shapes, or stick to just outlines. (If anyone wants
to rewrite ShapeStim to use glu tesselators that would be great!)
"""
win = visual.Window([600,600], monitor='testMonitor', units='norm')

arrowVertices=[ [-0.2,0.05], [-0.2,-0.05], [0.0,-0.05], [0.0,-0.1], [0.2,0], [0.0,0.1],  [0.0,0.05] ]
sqrVertices = [ [0.2,-0.2], [-0.2,-0.2], [-0.2,0.2], [0.2,0.2] ]

stim1 = visual.ShapeStim(win, 
                 lineRGB=[1,-1,-1],
                 lineWidth=2.0, #in pixels
                 fillRGB=None, #beware, with convex shapes this won't work
                 vertices=arrowVertices,#choose something from the above or make your own
                 closeShape=True,#do you want the final vertex to complete a loop with 1st?
                 pos= [0,0], #the anchor (rotaion and vertices are position with respect to this)
                 interpolate=True,
                 opacity=0.9)

stim2 = visual.ShapeStim(win, 
                 lineRGB=[-1,1,-1],
                 lineWidth=2.0, #in pixels
                 fillRGB=[-0.5,0.5,-0.5], #beware, with convex shapes this won't work
                 vertices=sqrVertices,#choose something from the above or make your own
                 closeShape=True,#do you want the final vertex to complete a loop with 1st?
                 pos= [0.5,0.5], #the anchor (rotaion and vertices are position with respect to this)
                 interpolate=True,
                 opacity=0.9)

while True:
    stim1.setOri(2,'+')
    stim1.draw()
    stim2.draw()
 
    win.flip()
    if len(event.getKeys()):
        core.quit()