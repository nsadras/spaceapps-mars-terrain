import bpy
import urllib
import urllib.request
import numpy as np

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

altitude_url_template = "https://api.nasa.gov/mars-wmts/catalog/Mars_MGS_MOLA_DEM_mosaic_global_463m_8/1.0.0/default/default028mm/{0}/{1}/{2}.png" 
texture_url_template = "https://api.nasa.gov/mars-wmts/catalog/Mars_Viking_MDIM21_ClrMosaic_global_232m/1.0.0/default/default028mm/{0}/{1}/{2}.png" 


def get_image(lat, lon):
    col = np.floor((lon - mapStartLon)/tileWidth);
    row = np.floor( (mapHeightInDegree - (lat + mapStartLat)) /tileHeight);
    altitude_url = altitude_url_template.format(int(maximumZoom), int(row), int(col));
    texture_url = texture_url_template.format(int(maximumZoom), int(row), int(col));

    print("altitude: {0}".format(altitude_url))
    print("texture: {0}".format(texture_url))

    dirpath = os.path.dirname(bpy.data.filepath)
    altitude_filename = os.path.join(dirpath, "{0}_{1}_altitude.png".format(lat, lon))
    texture_filename = os.path.join(dirpath, "{0}_{1}_texture.png".format(lat, lon))
    urllib.request.urlretrieve(altitude_url, altitude_filename)
    urllib.request.urlretrieve(texture_url, texture_filename)

def render_tile(lat, lon):
    altitude_filename = "{0}_{1}_altitude.png".format(lat, lon)
    texture_filename = "{0}_{1}_texture.png".format(lat, lon)

    dirpath = os.path.dirname(bpy.data.filepath)
    texture_filename = os.path.join(dirpath, texture_filename)

    try:
        img = bpy.data.images.load(texture_filename)
    except:
        raise NameError("Cannot load image %s" % realpath)
 
    # Create image texture from image
    cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
    cTex.image = img
 

    # Create material
    mat = bpy.data.materials.new('TexMat')
 
    # Add texture slot for color texture
    mtex = mat.texture_slots.add()
    mtex.texture = cTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.use_map_color_emission = True 
    mtex.emission_color_factor = 0.5
    mtex.use_map_density = True 
    mtex.mapping = 'FLAT'

    # Import surface height map as plane
    bpy.ops.import_image.to_plane(files=[{"name":altitude_filename, "name":altitude_filename}], directory="/Users/nsadras/Documents/spaceapps/", filter_image=True, filter_movie=True, filter_glob="", relative=False)

    # Add material to current object
    ob = bpy.context.object
    me = ob.data
    me.materials.clear()
    me.materials.append(mat)

    # Surface displacement
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=300)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_add(type="DISPLACE")

    #objname = filename.split(".")[0]
    objname = "{0}_{1}_altitude".format(lat, lon)
    bpy.data.objects[objname].modifiers['Displace'].texture = bpy.data.textures[objname]
    #bpy.data.objects['tile'].modifiers['Displace'].texture_coords = 'OBJECT'
    #bpy.data.objects['tile'].modifiers['Displace'].strength = 3.5
    #bpy.data.objects['tile'].modifiers['Displace'].mid_level = .1
    bpy.ops.object.shade_smooth()
    #bpy.ops.transform.resize(value=(8.48719, 8.48719, 8.48719), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

def main():
    lat = 0 # -90 to 90
    lon = 0 # -180 to 180
    filename = 'tile4.png'
    get_image(lat, lon)
    render_tile(lat, lon)
main()
