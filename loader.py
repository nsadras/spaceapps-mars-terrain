import os
import bpy

print("hello")
dirpath = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dirpath, "mars.py")

print(filename)
exec(compile(open(filename).read(), filename, 'exec'))

