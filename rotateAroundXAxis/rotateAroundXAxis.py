
import adsk.core, adsk.fusion, traceback,math
circles = None


#equation gets gets the value of function at a point
def equation(x):
	#return math.pow(10*x,0.5)

	 if x >= 5:
	 	return -1*math.pow(x-5,2)+5
	 else:
	 	return x

	#return 1/(x-5)

#draws circle cross section for start pos to end pos
def create3DModel(app,start,end):

	#reterving fusion 360 objects
	design = app.activeProduct
	
	rootComp = design.rootComponent

	sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

	circles = sketch.sketchCurves.sketchCircles

	ui  = app.userInterface

	lofts = rootComp.features.loftFeatures

	loftInput = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

	loftInput.isSolid = True
	
	#profiles list stoes every cross section
	profiles = []

	position = start

	#While gets every cross section between start position to end position
	while position < end:

		try:

			radius = round(equation(position), 5)

			#when radius = 0, an error occurs in fusion 360; a number really close to 0 works just as good 0
			if radius == 0:
				radius = 0.01

			circle = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,position),abs(radius))

			prof = sketch.profiles.item(len(profiles))
			profiles.append(prof)

		except Exception as e:
			pass
	
		position+= 0.1

		#rounds the position value to 2 digits
		position = round(position, 2)

	#each cross section is connected to eachother creating the 3d model of the fuction roated around the x axis
	try:
		for profile in profiles:
			loftInput.loftSections.add(profile)
	except:
		pass
	ext = lofts.add(loftInput)
		

#fustioon 360 runs the run fuction
def run(context):

	try:
		app = adsk.core.Application.get()

		#creates the 3d model from the starting pos to end pos
		create3DModel(app,0,10)

	except Exception as e:
		if ui:
			ui.messageBox('Failed:\n{}'.format(e))