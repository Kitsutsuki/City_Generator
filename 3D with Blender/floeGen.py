from bpy import *
from math import *
from random import *
from tools import *

def floeGenerator(floeW, floeH, hillsNum, hillSize, river):

	# 1 : générer une grille à partir des dimensions de la ville
	grid = []

	for i in range(0, floeW):
		for j in range(0, floeH):
			grid.append((i, j, 0));
			snow((i, j, 0))

	# 2 : définir la(les) colline(s)

	hill = []

	for c in range(0, hillsNum):
		r = randint(0, len(grid) - 1)
		hill.append(grid[r])

	# 3 : générer des blocs de glace

	def distance(p, c):
		return sqrt((p[0] - c[0]) * (p[0] - c[0]) + (p[1] - c[1]) * (p[1] - c[1]))

	isIceBlock = False

	for point in grid:
		for c in hill:
			d = distance(point, c) 
			r = sqrt(hillSize * floeW * floeH / pi) / 2
			if(d < r):
				isIceBlock = True
				break
			else:
				isIceBlock = False
		
		if(isIceBlock):
			h = fabs(uniform(cos(d * pi / 2 / r), cos(d * pi / 2 / r) + 0.5))
			iceBlock(point, h)
				

	ops.object.select_all(action='TOGGLE')
	ops.object.select_all()
	ops.object.join()
	
	return context.scene.objects.active