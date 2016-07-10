from bpy import *
from math import *
from random import *

def material(type):
	if(type == "Grass"):
		mat = data.materials.new("Grass")
		mat.diffuse_color = (uniform(0.01, 0.03), uniform(0.05, 0.12), 0)
	elif(type == "Sand"):
		mat = data.materials.new("Sand")
		mat.diffuse_color = (0.8, uniform(0.5, 0.55), 0.1)
	elif(type == "Water"):
		mat = data.materials.new("Water")
		mat.diffuse_color = (0, uniform(0.01, 0.03), uniform(0.01, 0.1))
	elif(type == "Oasis"):
		mat = data.materials.new("Oasis")
		mat.diffuse_color = (0, uniform(0.01, 0.03), uniform(0.3, 0.4))
	elif(type == "House"):
		mat = data.materials.new("House")
		mat.diffuse_color = (uniform(0.1, 0.3), uniform(0.01, 0.03), 0)
	elif(type == "DesertHouse"):
		mat = data.materials.new("DesertHouse")
		mat.diffuse_color = (uniform(0.8, 0.9), uniform(0.6, 0.7), 0.3)
	elif(type == "Road"):
		mat = data.materials.new("Road")
		r = uniform(0.1, 0.2)
		mat.diffuse_color = (r, r, r + 0.02)
	elif(type == "DesertRoad"):
		mat = data.materials.new("DesertRoad")
		mat.diffuse_color = (0.9, uniform(0.6, 0.65), 0.2)
	elif(type == "Building"):
		mat = data.materials.new("Building")
		r = uniform(0.01, 0.05)
		mat.diffuse_color = (r, r, r + 0.005)
	elif(type == "Tree"):
		mat = data.materials.new("Trunk")
		mat.diffuse_color = (uniform(0, 0.03), uniform(0.03, 0.05), 0)
	elif(type == "DesertTree"):
		mat = data.materials.new("Trunk")
		mat.diffuse_color = (uniform(0.1, 0.3), uniform(0.01, 0.03), uniform(0.01, 0.03))
	elif(type == "Snow"):
		mat = data.materials.new("Snow")
		mat.diffuse_color = (uniform(0.85, 0.9), uniform(0.85, 0.9), uniform(0.95, 1))
	return mat

def house(houseWidth, baseCenter):
	grass(baseCenter, False)
	verts = [(-0.5,-0.5,0), (-0.5,-0.5,1), (-0.5,0.5,0), (-0.5,0.5,1), (0.5,-0.5,0), (0.5,-0.5,1), (0.5,0.5,0), (0.5,0.5,1), (0,-0.5,1.5), (0,0.5,1.5)]
	edges = [(0,4), (1,5), (0,1), (4,5), (2,3), (6,7), (6,2), (3,7), (1,3), (0,2), (4,6), (5,7), (1,8), (8,5), (3,9), (9,7), (8,9)]
	faces = [(0,4,5,1), (2,3,7,6), (0,1,3,2), (4,6,7,5), (0,2,6,4), (1,8,9,3), (5,7,9,8), (1,5,8), (3,9,7)]
	#creation de mesh
	houseMesh = data.meshes.new("houseMesh")
	houseMesh.from_pydata(verts, edges, faces)
	houseObject = data.objects.new("houseObject", houseMesh)
	context.scene.objects.link(houseObject)	
	context.scene.objects.active = houseObject
	context.scene.objects.active.data.materials.append(material("House"))
	for o in context.scene.objects:
		o.select = False
	houseObject.select = True
	housePosition = (baseCenter[0], baseCenter[1], baseCenter[2])
	minX = baseCenter[0] - 0.5
	maxX = baseCenter[0] + 0.5
	minY = baseCenter[1] - 0.5
	maxY = baseCenter[1] + 0.5
	newX = uniform(minX, maxX)
	newY = uniform(minY, maxY)
	if(newX - houseWidth/2 < -0.5):
		newX = -0.5 + houseWidth
	if(newX + houseWidth/2 > 0.5):
		newX = 0.5 - houseWidth
	if(newY- houseWidth/2 < -0.5):
		newY = -0.5 + houseWidth
	if(newY + houseWidth/2 > 0.5):
		newY = 0.5 - houseWidth
	housePosition = (newX,newY,0)
	ops.transform.translate(value=baseCenter)
	ops.transform.resize(value=(houseWidth, houseWidth, houseWidth))
	orientation = randint(0,1)
	ops.transform.rotate(value=orientation * pi / 2, axis=(0,0,1))
	
def desertHouse(location):
	sand(location, False)
	r = uniform(0.3,0.5)
	ops.mesh.primitive_cube_add(radius=r, location=(location[0], location[1], r))
	context.scene.objects.active.data.materials.append(material("DesertHouse"))
	
def grass(location, withTree=True):
	ops.mesh.primitive_plane_add(radius=0.5, location=location)
	context.scene.objects.active.data.materials.append(material("Grass"))
	if(withTree):
		r = randint(0, 4)
		if(r == 0):
			tree(location)
	
def sand(location, withTree=True):
	ops.mesh.primitive_plane_add(radius=0.5, location=location)
	context.scene.objects.active.data.materials.append(material("Sand"))
	if(withTree):
		r = randint(0, 19)
		if(r == 0):
			desertTree(location)
	
def road(location):
	ops.mesh.primitive_plane_add(radius=0.5, location=location)
	context.scene.objects.active.data.materials.append(material("Road"))
	
def desertRoad(location):
	ops.mesh.primitive_plane_add(radius=0.5, location=location)
	context.scene.objects.active.data.materials.append(material("DesertRoad"))
	
def water(location):
	ops.mesh.primitive_plane_add(radius=0.5, location=location)
	context.scene.objects.active.data.materials.append(material("Water"))
	
def oasis(location):
	ops.mesh.primitive_plane_add(radius=0.5, location=location)
	context.scene.objects.active.data.materials.append(material("Oasis"))

def building(location, height):
	ops.mesh.primitive_plane_add(radius = 0.5, location=location)
	ops.object.mode_set(mode='EDIT')
	ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten={"value":-height})
	ops.object.mode_set(mode='OBJECT')
	context.scene.objects.active.data.materials.append(material("Building"))
	
def tree(location):
	ops.curve.tree_add(do_update=True, chooseSet='0', bevel=True, prune=False, seed=randint(0,10), handleType='1', levels=2, length=(0.8, 0.5, 1.5, 0.1), lengthV=(0, 0.1, 0, 0), branches=(0, 25, 10, 300), curveRes=(8, 16, 12, 1), curve=(0, 40, 0, 0), curveV=(120, 90, 0, 0), curveBack=(20, 80, 0, 0), baseSplits=2, segSplits=(0.1, 0.2, 0.2, 0), splitAngle=(3, 30, 45, 0), splitAngleV=(0, 10, 20, 0), scale=15, scaleV=5, attractUp=-3, shape='3', baseSize=0.05, ratio=0.03, taper=(1, 1, 1, 1), ratioPower=2, downAngle=(0, 20, 30, 20), downAngleV=(0, 10, 10, 10), rotate=(0, -120, -120, 140), rotateV=(0, 30, 30, 0), scale0=1, scaleV0=0, bend=0, bevelRes=0, resU=4, frameRate=1, windSpeed=2, windGust=0, armAnim=False, startCurv=0)
	context.scene.objects["tree"].location = location
	context.scene.objects["tree"].scale = (0.1, 0.1, 0.1)
	context.scene.objects["tree"].data.materials.append(material("Tree"))
	context.scene.objects.active = context.scene.objects["tree"]
	context.scene.objects["tree"].select = True
	ops.object.convert(target='MESH')
	context.scene.objects["tree"].name = "MyTree"
	
def desertTree(location):
	ops.curve.tree_add(do_update=True, chooseSet='0', bevel=True, prune=False, seed=randint(0,10), handleType='1', levels=2, length=(0.8, 0.5, 1.5, 0.1), lengthV=(0, 0.1, 0, 0), branches=(0, 25, 10, 300), curveRes=(8, 16, 12, 1), curve=(0, 40, 0, 0), curveV=(120, 90, 0, 0), curveBack=(20, 80, 0, 0), baseSplits=2, segSplits=(0.1, 0.2, 0.2, 0), splitAngle=(3, 30, 45, 0), splitAngleV=(0, 10, 20, 0), scale=15, scaleV=5, attractUp=-3, shape='3', baseSize=0.05, ratio=0.03, taper=(1, 1, 1, 1), ratioPower=2, downAngle=(0, 20, 30, 20), downAngleV=(0, 10, 10, 10), rotate=(0, -120, -120, 140), rotateV=(0, 30, 30, 0), scale0=1, scaleV0=0, bend=0, bevelRes=0, resU=4, frameRate=1, windSpeed=2, windGust=0, armAnim=False, startCurv=0)
	context.scene.objects["tree"].location = location
	context.scene.objects["tree"].scale = (0.1, 0.1, 0.1)
	context.scene.objects["tree"].data.materials.append(material("DesertTree"))
	context.scene.objects.active = context.scene.objects["tree"]
	context.scene.objects["tree"].select = True
	ops.object.convert(target='MESH')
	context.scene.objects["tree"].name = "MyTree"
	
def snow(location):
	ops.mesh.primitive_plane_add(radius=0.5, location=location)
	context.scene.objects.active.data.materials.append(material("Snow"))
	
def iceBlock(location, height):
	ops.mesh.primitive_plane_add(radius = 0.5, location=location)
	ops.object.mode_set(mode='EDIT')
	ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten={"value":-height})
	ops.object.mode_set(mode='OBJECT')
	context.scene.objects.active.data.materials.append(material("Snow"))

def addCamera(x, y):
	ops.object.camera_add(location=(-(x - 1) / 2, -(y - 1) * 2, y * 2 / 3), rotation=(pi / 3, 0, 0))
	
def distance(p, c):
	return sqrt((p[0] - c[0]) * (p[0] - c[0]) + (p[1] - c[1]) * (p[1] - c[1]))