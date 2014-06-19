from bpy import *
from math import *
from random import *
from tools import *

def desertGenerator(desertW, desertH, villagesNum, villageSize, isRoad):
	
	# 1 : g�n�rer une grille � partir des dimensions de la carte
	grid = []

	for i in range(0, desertW):
		for j in range(0, desertH):
			grid.append((i, j, 0));

	# 2 : g�n�rer une route (facultatif)
	
	roadPoints = []
	
	if(isRoad):	
	
		x = randint(0,1)
		y = randint(0,1)
		
		# direction g�n�rale de la route : 0 = vers le haut, 1 = vers le bas, 2 = vers la gauche, 3 = vers la droite
		roadDir = randint(0,1);
		
		# coordonn�es du premier bloc de route (� une des extr�mit�s de la carte)
		if(roadDir == 0):
			# Direction verticale
			roadX = 0
			roadY = randint(0,desertH)
			grid.remove((roadX, roadY, 0))
			desertRoad((roadX, roadY, 0))
			while(roadX <= desertW):
				nextBlock = randint(0,9)
				if(nextBlock >= 0 and nextBlock <= 7):
					roadX = roadX + 1
				elif(nextBlock == 8):
					roadY = roadY + 1
				else:
					roadY = roadY - 1
					
				if((roadX, roadY, 0) in grid):
					grid.remove((roadX, roadY, 0))
					desertRoad((roadX, roadY, 0))
					roadPoints.append((roadX, roadY, 0))
				else:
					continue
		else:
			# Direction horizontale
			roadX = randint(0, desertW)
			roadY = 0
			grid.remove((roadX, roadY, 0))
			desertRoad((roadX, roadY, 0))
			while(roadY <= desertW + 1):
				nextBlock = randint(0,9)
				if(nextBlock >= 0 and nextBlock <= 7):
					roadY = roadY + 1
				elif(nextBlock == 8):
					roadX = roadX + 1
				else:
					roadX = roadX - 1
					
				if((roadX, roadY, 0) in grid):
					grid.remove((roadX, roadY, 0))
					desertRoad((roadX, roadY, 0))
					roadPoints.append((roadX, roadY, 0))
				else:
					continue

	#3 : d�finir l'oasis
	
	oasisX = randint(0,desertW)
	oasisY = randint(0,desertH)

	for point in roadPoints:
		while(distance(point, (oasisX, oasisY, 0)) < sqrt(villageSize * desertW * desertH / pi ) / 2):
			oasisX = randint(0,desertW)
			oasisY = randint(0,desertH)
					
	# 4 : d�finir le(s) village(s) 

	village = []

	for c in range(0, villagesNum):
		r = randint(0, len(grid) - 1)
		village.append(grid[r])


	# 5 : g�n�rer des b�timents sur les points de la grille qui restent

	farm = False

	for point in grid:
		for c in village:
			if(distance(point, c) < sqrt(villageSize * desertW * desertH / pi ) / 2):
				farm = True
				break
			else:
				farm = False
		
		if(distance(point, (oasisX, oasisY, 0)) < sqrt(villageSize * desertW * desertH / pi ) / 2):
			oasis(point)
		
		elif(farm):
			r = randint(0,2)
			if(r == 0 or r == 1):
				desertHouse(point)
			elif(r == 2):
				sand(point)

		else:
			sand(point)

	ops.object.select_all(action='TOGGLE')
	ops.object.select_all()
	ops.object.join()
	
	return context.scene.objects.active