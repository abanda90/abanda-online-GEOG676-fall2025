# -*- coding: utf-8 -*-

import time
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Graduated Color"
        self.description = "create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        #layer to be used to classify to create the color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )
        #output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            direction="Input",
        )
        #output project name
        param3 = arcpy.Parameter(
            displayName= "Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
        return params

        #Licensed, Parameters, and Messages do not need to be changed
    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define Progressor Values
        readTime = 3 #the time for users to read the progress
        start = 0   #beginning position of the progressor
        max = 100   # end position
        step = 33   # the progress interval to move th progressor along

        # Set up Progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) #pause the execution for 3 seconds

        # Add Message to the Results Pane
        arcpy.AddMessage("Validating Project File")

        # Project file 
        Project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        #Grabs the First Instance of a Map from the .aprx
        campus = Project.listMaps('Map')[0]
        target_name = arcpy.Describe(parameters[1].value).name
        target_desc = arcpy.Describe(parameters[1].value)
        target_path = target_desc.catalogPath

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step) #now is 33% complete
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        #loop through the layers of the map
        for layer in campus.listLayers():
            #check if the layer is a feature layer
            if layer.isFeatureLayer:
                #copy layer's symbology
                symbology = layer.symbology
                # make sure the symbology has renderer attribute
                if hasattr(symbology, 'renderer'):
                    #check layer name
                    if arcpy.Describe(layer).catalogPath == target_path:
                        
        #increment progressor
                        arcpy.SetProgressorPosition(start + step*2) #now is 66% complete
                        arcpy.SetProgressorLabel("Calculating and Classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculate and Classifying...")

                    #update the copy's renderer to "Graduated Colors Renderer"
                    symbology.updateRenderer('GraduatedColorsRenderer')

                      # choose a valid area field if present
                    numeric_fields = [f.name for f in arcpy.ListFields(layer)
                                      if f.type in ("Double", "Single", "Integer", "SmallInteger")]
                    class_field = None
                    for cand in ("Shape_Area", "SHAPE_Area", "Shape__Area"):
                        if cand in numeric_fields:
                            class_field = cand
                            break
                    if class_field is None:
                        raise arcpy.ExecuteError(
                            f"Layer '{target_name}' has no 'Shape_Area' field. "
                            f"Numeric fields available: {numeric_fields}"
                        )

                    #tell arcpy based on which field we want to base our chloropleth off of
                    symbology.renderer.classificationField = class_field

                    #set how many classes we will have for the map
                    symbology.renderer.breakCount = 5

                    #set color ramp
                    symbology.renderer.colorRamp = Project.listColorRamps('Oranges (5 classes)') [0]

                    #set the layer's Actual Symbology Equal to the Copy's
                    layer.symbology = symbology

                    arcpy.AddMessage("Finish Generating Layer...")
                    
                    break
                else: 
                    print("Layer Not Found")

            # Increment Progressor
            arcpy.SetProgressorPosition(start + step*3) #now is 99% complete
            arcpy.SetProgressorLabel("Saving...")
            time.sleep(readTime)
            arcpy.AddMessage("Saving...")

        Project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")
        #param  2 is the folder location and param 3 is the name of the new project
        return         

