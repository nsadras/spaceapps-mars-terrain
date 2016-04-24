import bpy
import urllib
import urllib.request
import numpy as np

lat = 0 # -90 to 90
lon = 0 # -180 to 180

# Constants
mapWidthInDegree = 360.0
mapHeightInDegree = 180.0
mapStartLon = -180.0
mapStartLat = 90.0
pixelTileWidth = 256
pixelTileHeight = pixelTileWidth

maximumZoom = 3
elevationOffset = -8201
elevationScale = 115.4588

tileWidth = mapWidthInDegree/pow(2, maximumZoom+1);
tileHeight = tileWidth;

api_url = "https://api.nasa.gov/mars-wmts/catalog/Mars_MGS_MOLA_DEM_mosaic_global_463m_8/1.0.0/default/default028mm/{0}/{1}/{2}.png" 

def get_image(lat, lon, dest_file):
    col = np.floor((lon - mapStartLon)/tileWidth);
    row = np.floor( (mapHeightInDegree - (lat + mapStartLat)) /tileHeight);
    imageURL = api_url.format(int(maximumZoom), int(row), int(col));

    print(imageURL)
    dirpath = os.path.dirname(bpy.data.filepath)
    filename = os.path.join(dirpath, dest_file)
    urllib.request.urlretrieve(imageURL, filename)

def render_tile(filename):
    bpy.ops.import_image.to_plane(files=[{"name":filename, "name":filename}], directory="/Users/nsadras/Documents/spaceapps/", filter_image=True, filter_movie=True, filter_glob="", relative=False)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=300)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_add(type="DISPLACE")

    objname = filename.split(".")[0]
    bpy.data.objects[objname].modifiers['Displace'].texture = bpy.data.textures[objname]
    #bpy.data.objects['tile'].modifiers['Displace'].texture_coords = 'OBJECT'
    #bpy.data.objects['tile'].modifiers['Displace'].strength = 3.5
    #bpy.data.objects['tile'].modifiers['Displace'].mid_level = .1
    #bpy.ops.object.shade_smooth()

filename = 'tile.png'
get_image(lat, lon, filename)
render_tile(filename)
