# create a gdb and garage feature
import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [BuildingProximity]

class BuildingProximity(object):


class Tool(object):

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
    param0 = arcpy.Parameter(
        displayName="GDB Folder",
        name="GDBFOLDER",
        datatype="DeFolder",
        parameterType="Required",
        direction="Input"
    )
    param1 = arcpy.Parameter(
        displayName="GDB Name",
        name="GDBName",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
    )
    param2 = arcpy.Parameter(
        displayName= "Garage CSV File",
        name="GarageCSVFile",
        datatype="DEFile",
        parameterType="Required",
        direction="Input"
    )
    param3 = arcpy.Parameter(
        displayName="Garage Layer Name",
        name="GarageLayerName",
        datatype="GPSString",
        parameterType="Required",
        direction="Input"
    )
    param4 = arcpy.Parameter(
        displayName="Campus GDB",
        name= "CampusGDB",
        datatype="DEType",
        parameterType="Required",
        direction="Input"
    )
    param5 = arcpy.Parameter(
        displayName="Buffer Distance",
        name= "BufferDistance",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input"
    )
    params = [param0, param1, param2, param3, param4, param5]
    return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

   def updateParameters(self, parameters):
    # Set the default distance threshold to 1/100 of the larger of the width
    #  or height of the extent of the input features.  Do not set if there is no 
    #  input dataset yet, or the user has set a specific distance (Altered is true).
    #
    if parameters[0].valueAsText:
        if not parameters[6].altered:
            extent = arcpy.Describe(parameters[0]).extent
        if extent.width > extent.height:
            parameters[6].value = extent.width / 100
        else:
            parameters[6].value = extent.height / 100

    return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
