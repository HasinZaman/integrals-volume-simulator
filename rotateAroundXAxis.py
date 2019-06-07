
import adsk.core, adsk.fusion, traceback,math
circles = None



def equation(x):
	#insert equation in here
	#return math.pow(10*x,0.5)

	# if x >= 5:
	# 	return -1*math.pow(x-5,2)+5
	# else:
	# 	return x

	return 1/(x-5)

def drawCylinder(app,start,end):
	design = app.activeProduct
	rootComp = design.rootComponent

	sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

	circles = sketch.sketchCurves.sketchCircles

	

	ui  = app.userInterface

	
	profiles = []
	position = start
	while position <end:
		try:
			#ui.messageBox("{0}||{1}".format(x,abs(equation(x))))
			radius = equation(position)
			if radius == 0:
				radius = 0.1
			circle = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,position),abs(radius))
			prof = sketch.profiles.item(len(profiles))
			profiles.append(prof)
		except Exception as e:
			pass
			#profiles.append(None)
		position+= 0.1

		position = round(position, 2)

	ui.messageBox("done")

	lofts = rootComp.features.loftFeatures

	loftInput = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

	loftInput.isSolid = True

	try:
		for profile in profiles:
			loftInput.loftSections.add(profile)


		ext = lofts.add(loftInput)
	except Exception as e:
		ui.messageBox(str(e))		
		

	
def run(context):
    ui = None

    try:
        app = adsk.core.Application.get()

        drawCylinder(app,0,10)

    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(e))