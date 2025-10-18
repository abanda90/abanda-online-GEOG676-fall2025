import arcpy

#assign bands
source = r"C:\abanda-online-GEOG676-fall2025\Lab7\Imagery"

band1 = arcpy.sa.Raster(source + r"\band1.TIF") #blue
band2 = arcpy.sa.Raster(source + r"\band2.TIF") #green
band3 = arcpy.sa.Raster(source + r"\band3.TIF") #red
band4 = arcpy.sa.Raster(source + r"\band4.TIF") #NIR
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\output_combined.tif")

#hillshade
azimuth = 315
altitude = 45
shadows = 'NO_SHADOWS'
z_factor = 1
arcpy.ddd.HillShade(source + r"\DEM.TIF", source + r"\output_Hilshade.tif", azimuth, altitude, shadows, z_factor)

#slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(source + r"\DEM.TIF", source + r"\output_Slope.tif",output_measurement, z_factor)

print("Success! You completed Lab 7!")
