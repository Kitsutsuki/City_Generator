from bpy import *
from bpy.props import *
from random import *
from math import *
from countryGen import *
from cityGen import *
from desertGen import *
from floeGen import *

def initPan(scn) :
	types.Scene.MyName = StringProperty(name = "Name ",
	description = "Nom de la structure ?",)
	scn['MyName'] = "TownGen"

	types.Scene.MyMilieu = EnumProperty(name = "Milieu",
	items = [('URBAIN','Urbain','',1),('RURAL','Rural','',2), ('DESERT','Désert','',3), ('BANQUISE','Banquise','',4)])
	scn['MyMilieu'] = 1
	
	types.Scene.PosX = StringProperty(name = "X ",
	description = "Position en X ?",)
	scn['PosX'] = "0"
	
	types.Scene.PosY = StringProperty(name = "Y ",
	description = "Position en Y ?",)
	scn['PosY'] = "0"
	
	types.Scene.PosZ = StringProperty(name = "Z ",
	description = "Position en Z ?",)
	scn['PosZ'] = "0"

	types.Scene.MyCityW = IntProperty(
	name = "Width", 
	description = "Largeur de la ville ?",
	min = 10,max = 50)
	scn['MyCityW'] = 10

	types.Scene.MyCityH = IntProperty(
	name = "Length", 
	description = "Longeur de la ville ?",
	min = 10,max = 50)
	scn['MyCityH'] = 10

	types.Scene.MyRoadDensity = IntProperty(
	name = "Density", 
	description = "Densité de route ?",
	min = 1)
	scn['MyRoadDensity'] = 4

	types.Scene.MyNbTown = IntProperty(
	name = "NbTown", 
	description = "Nombre de villes ?",
	min = 0)
	scn['MyNbTown'] = 4

	types.Scene.MySizeTown = FloatProperty(
	name = "SizeTown", 
	description = "Taille de ville ?",
	min = 0.05,max = 0.5)
	scn['MySizeTown'] = 0.5

	types.Scene.MyRiver = BoolProperty(
	name = "river",
	description = "Présence d'une rivière?")
	scn['MyRiver'] = False
	
	return

initPan(context.scene)
	
class UIPanel(types.Panel) :
	bl_label = "L-System Panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
 
	def draw(self, context):
		layout = self.layout
		scn = context.scene

		layout.prop(scn, 'MyName')
		layout.prop(scn, 'MyMilieu')
		
		layout.label("Position : ")
		box = layout.box()
		row = box.row(align=True)
		row.prop(scn, 'PosX')
		row.prop(scn, 'PosY')
		row.prop(scn, 'PosZ')
		
		layout.prop(scn, 'MyCityW')
		layout.prop(scn, 'MyCityH')
		layout.prop(scn, 'MyNbTown')
		layout.prop(scn, 'MySizeTown')
		layout.prop(scn, 'MyRoadDensity')
		layout.prop(scn, 'MyRiver')

		row = layout.row(align=True)
		row.operator("exe.rand", text="Random")
		row.operator("exe.init", text="Reset")
		
		row = layout.row(align=False)
		row.operator("exe.run", text="Execute")

class OBJECT_OT_PrintPropsButton(types.Operator) :	  
	bl_idname = "exe.run"
	bl_label = "Execute"
	
	def execute(self,context) :
		scn = context.scene
		context.scene.cursor_location = (float(scn['PosX']),float(scn['PosX']),float(scn['PosX']))

		if(scn['MyMilieu'] == 1):
			obj = cityGenerator(int(scn['MyCityW']), int(scn['MyCityH']), int(scn['MyRoadDensity']), int(scn['MyNbTown']), float(scn['MySizeTown']), bool(scn['MyRiver']))
		elif(scn['MyMilieu'] == 2):
			obj = countryGenerator(int(scn['MyCityW']), int(scn['MyCityH']), int(scn['MyRoadDensity']), int(scn['MyNbTown']), float(scn['MySizeTown']), bool(scn['MyRiver']))
		elif(scn['MyMilieu'] == 3):
			obj = desertGenerator(int(scn['MyCityW']), int(scn['MyCityH']), int(scn['MyNbTown']), float(scn['MySizeTown']), bool(scn['MyRiver']))
		else:
			obj = floeGenerator(int(scn['MyCityW']), int(scn['MyCityH']), int(scn['MyNbTown']), float(scn['MySizeTown']), bool(scn['MyRiver']))
		
		addCamera(int(scn['MyCityW']), int(scn['MyCityH']))
		
		obj.name = scn['MyName']
		return{'FINISHED'}

class OBJECT_OT_InitPropsButton(types.Operator) :
	bl_idname = "exe.init"
	bl_label = "Init"
	
	def execute(self,context) :
		scn = context.scene
		
		scn['MyName'] = "TownGen"
		scn['MyMilieu'] = 1
		scn['PosX'] = "0"
		scn['PosY'] = "0"
		scn['PosZ'] = "0"
		scn['MyCityW'] = 10
		scn['MyCityH'] = 10
		scn['MyRoadDensity'] = 4
		scn['MyNbTown'] = 4
		scn['MySizeTown'] = 0.5
		scn['MyRiver'] = False
		return{'FINISHED'}

class OBJECT_OT_InitPropsButton(types.Operator) :
	bl_idname = "exe.rand"
	bl_label = "Rand"
	
	def execute(self,context) :
		scn = context.scene
		
		scn['MyName'] = "TownGen"
		scn['MyMilieu'] = randint(1,4)
		scn['MyRoadDensity'] = randint(1,floor(int(scn['MyCityW'])+int(scn['MyCityW'])/10))
		scn['MyNbTown'] = randint(1,5)
		scn['MySizeTown'] = uniform(0.05,0.2)
		scn['MyRiver'] = randint(0,1)
		return{'FINISHED'}
	
utils.register_module(__name__)