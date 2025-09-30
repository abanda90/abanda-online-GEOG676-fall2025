# Lab 5 Creating a toolbox in ArcGIS Pro
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
    pass


class BuildingProximity(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5 Toolbox"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFOLDER",
            datatype="DEFolder",
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
            datatype="GPString",  
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name= "CampusGDB",
            datatype="DEWorkspace",  
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
        try:
            if parameters[0].valueAsText:
                if not parameters[5].altered:
                    desc = arcpy.Describe(parameters[0].valueAsText)
                    extent = getattr(desc, "extent", None)
                    if extent:
                        parameters[5].value = (extent.width if extent.width > extent.height else extent.height) / 100.0
        except Exception:
            pass
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        folder_path = r'C:\abanda-online-GEOG676-fall2025\Lab4'
        gdb_name = 'Test.gdb'
        gdb_path = folder_path + '\\' + gdb_name
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        csv_path = r'C:\abanda-online-GEOG676-fall2025\Lab4\garages.csv'
        garage_layer_name = 'Garage_Points'
        garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + '\\' + garage_layer_name

        # open campus gdb, copy building feature to our gdb
        campus = r'c:\abanda-online-GEOG676-fall2025\Lab4\Campus.gdb'  
        buildings_campus = campus + '\\Structures'  
        buildings = gdb_path + '\\' + 'Buildings'

        arcpy.Copy_management(buildings_campus, buildings)

        # reprojection
        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path + '\\Garage_Points_reprojected', spatial_ref)  

        # buffer the garages
        garageBuffered = arcpy.Buffer_analysis(gdb_path + '\\Garage_Points_reprojected', gdb_path + '\\Garage_Points_buffered', 150)  

        # Intersect our buffer with the buildings
        arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\\Garage_Building_Intersection', 'ALL')  

        arcpy.TableToTable_conversion(gdb_path + '\\Garage_Building_Intersection', r'C:\abanda-online-GEOG676-fall2025\Lab4', 'nearbybuildings.csv')  
