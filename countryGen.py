from bpy import *
from math import *
from random import *
from tools import *

def material(type):
	if(type == "Grass"):
		mat = data.materials.new("Grass")
		mat.diffuse_color = (uniform(0.01, 0.03), uniform(0.05, 0.12), 0)
	elif(type == "Water"):
		mat = data.materials.new("Water")
		mat.diffuse_color = (0, uniform(0.01, 0.03), uniform(0.01, 0.1))
	elif(type == "House"):
		mat = data.materials.new("House")
		mat.diffuse_color = (uniform(0.1, 0.3), uniform(0.01, 0.03), 0)
	elif(type == "Road"):
		mat = data.materials.new("Road")
		r = uniform(0.1, 0.2)
		mat.diffuse_color = (r, r, r + 0.02)
	return mat	

def countryGenerator(mapW, mapH, startBlocks, villagesNum, villageSize, river):

	# 1 : générer une grille à partir des dimensions de la carte
	grid = []

	for i in range(0, mapW):
		for j in range(0, mapH):
			grid.append((i, j, 0));

	# 2 : générer une rivière (facultatif)

	if(river == True):
		ok = False
		while ok == False:
			waterX = randint(0, mapW)
			waterY = randint(0, mapH)
			
			if((waterX, waterY, 0) in grid): 
				grid.remove((waterX, waterY, 0))
				water((waterX, waterY, 0))
				ok = True

		riverL = mapW + mapH

		for j in range(0, riverL):
			nextBlock = randint(0,9)
			if(nextBlock >= 0 and nextBlock <= 4):
				waterX = waterX
				waterY = waterY + 1
					
			elif(nextBlock == 5 or nextBlock == 6):
				waterX = waterX
				waterY = waterY - 1
					
			elif(nextBlock == 7 or nextBlock == 8):
				waterX = waterX + 1
				waterY = waterY
					
			elif(nextBlock == 9):
				waterX = waterX - 1
				waterY = waterY

			if((waterX, waterY, 0) in grid): 
				grid.remove((waterX, waterY, 0))
				water((waterX, waterY, 0))
			else:
				continue
			
	# 3 : générer des routes (carrés) sur les points de la grille

	for i in range (0, startBlocks):
		# coordonnées du premier bloc de route
		roadX = randint(0, mapW)
		roadY = randint(0, mapH)
		
		if((roadX, roadY, 0) in grid): 
			grid.remove((roadX, roadY, 0))
			road((roadX, roadY, 0))
		else:
			continue
		
		
		# longueur de la route
		roadL = randint((int)(mapW * mapH / (mapW + mapH)), (int) (mapW * mapH / (fabs(mapW - mapH) + 1)))

		# direction générale de la route : 0 = vers le haut, 1 = vers le bas, 2 = vers la gauche, 3 = vers la droite
		roadDir = randint(0,3);
		
		for j in range(0, roadL):
			nextBlock = randint(0,3)
			if(nextBlock == 0 or nextBlock == 1):
				if(roadDir == 0):
					# aller vers le haut
					roadX = roadX + 1
					roadY = roadY
				if(roadDir == 1):
					# aller vers le bas
					roadX = roadX - 1
					roadY = roadY
				if(roadDir == 2):
					# aller vers la gauche
					roadX = roadX
					roadY = roadY - 1
				if(roadDir == 3):
					# aller vers la droite
					roadX = roadX
					roadY = roadY + 1
					
			elif(nextBlock == 2):
				if(roadDir == 0):
					# aller vers la droite
					roadX = roadX
					roadY = roadY + 1
				if(roadDir == 1):
					# aller vers la gauche
					roadX = roadX
					roadY = roadY - 1
				if(roadDir == 2):
					# aller vers le haut
					roadX = roadX + 1
					roadY = roadY
				if(roadDir == 3):
					# aller vers le bas
					roadX = roadX - 1
					roadY = roadY
					
			elif(nextBlock == 3):
				if(roadDir == 0):
					# aller vers la gauche
					roadX = roadX
					roadY = roadY - 1
				if(roadDir == 1):
					# aller vers la droite
					roadX = roadX
					roadY = roadY + 1
				if(roadDir == 2):
					# aller vers le bas
					roadX = roadX - 1
					roadY = roadY
				if(roadDir == 3):
					# aller vers le haut
					roadX = roadX + 1
					roadY = roadY
		
			if((roadX, roadY, 0) in grid):
				print(roadX, roadY)
				grid.remove((roadX, roadY, 0))
				road((roadX, roadY, 0))
			else:
				continue


	# 4 : définir le(s) village(s) 

	village = []

	for c in range(0, villagesNum):
		r = randint(0, len(grid) - 1)
		village.append(grid[r])


	# 5 : générer des bâtiments sur les points de la grille qui restent

	def distance(p, c):
		return sqrt((p[0] - c[0]) * (p[0] - c[0]) + (p[1] - c[1]) * (p[1] - c[1]))

	farm = False

	for point in grid:
		for c in village:
			if(distance(point, c) < sqrt(villageSize * mapW * mapH / pi ) / 2):
				farm = True
				break
			else:
				farm = False
		
		if(farm):
			r = randint(0,2)
			h = uniform(3,5)
			if(r == 0):
				house(uniform(0.5, 0.9), point)
			elif(r == 1):
				house(uniform(0.6, 0.9), point)
			elif(r == 2):
				road(point)

		else:
			grass(point)
			context.scene.objects.active.data.materials.append(material("Grass"))

	ops.object.select_all(action='TOGGLE')
	ops.object.select_all()
	ops.object.join()
	
	return context.scene.objects.active