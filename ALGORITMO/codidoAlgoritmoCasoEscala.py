#CÓDIGO DEL ALGORITMO PARA EL PROYECTO MAJOR PIPING LAYOUT - PAI G2C - 2022-3 - UNAL

from astar.search import AStar
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fpdf import FPDF 
import xlsxwriter as xls
import pytz
from datetime import datetime



 # mapa rectangular de cualquier valor

"""
Como se ve así es el mapa en el que se mueve el algoritmo, una matriz rectangular/cuadrada donde 0 son posiciones disponibles y 1 son posiciones ocupadas.

world = [
        [0,0,0,0,0,0],
        [1,1,0,0,0,0],
        [0,0,0,1,0,0],
        [0,0,0,1,0,0],
        [0,0,0,1,0,0],
        [0,0,0,1,0,0],
        ]

print(world)
"""

largo = 12 #int(input("Introduzca el largo del área de trabajo: "))
ancho = 12 #int(input("Introduzca el ancho del área de trabajo: "))

world = np.zeros((largo,ancho))
newWorld=np.zeros((largo,ancho))
newWorld2=np.zeros((largo,ancho))

l = int(len(world))

anchopr = 10 #int(input("Introduzca el Ancho Piperack: ")) 

largopr = 10 #int(input("Introduzca el Largo Piperack: "))

altopr = 10 #int(input("Introduzca el Alto Piperack: "))

seccionespr = 3 #int(input("Introduzca el número de secciones del Piperack: "))
seccionespr += 1


fp = int(((l - largopr)//2))  #3

sp = int(l - ((l - largopr)//2)) #7

lin_piperack = []

for i in range(fp):
  world[i][fp-1] = 5
  newWorld[i][fp-1] = 5
  newWorld2[i][fp-1] = 5
  linea = (i,fp-1)
  lin_piperack.append(linea)
for j in range(sp,l,1):  
  world[j][fp-1] = 5
  newWorld[j][fp-1] = 5
  newWorld2[j][fp-1] = 5
  linea = (j,fp-1)
  lin_piperack.append(linea)
for h in range(fp):
  world[h][sp] = 5
  newWorld[h][sp] = 5
  newWorld2[h][sp] = 5
  linea = (h,sp)
  lin_piperack.append(linea)
for k in range(sp,l,1):
  world[k][sp] = 5
  newWorld[k][sp] = 5
  newWorld2[k][sp] = 5
  linea = (k, sp)
  lin_piperack.append(linea)
for o in range(fp, sp+1, 1):
  world[fp-1][o] = 5
  newWorld[fp-1][o] = 5
  newWorld2[fp-1][o] = 5
  linea = (fp-1, o)
  lin_piperack.append(linea)
for p in range(fp, sp+1, 1):
  world[sp][p] = 5
  newWorld[sp][p] = 5
  newWorld2[sp][p] = 5
  linea = (sp,p)
  lin_piperack.append(linea)


xp = [x[1] for x in lin_piperack]
yp = [y[0] for y in lin_piperack]

plotPiperackX = [fp, fp, sp, sp, fp]
plotPiperackY = [fp, sp, sp, fp, fp]

plotPiperackL1 = [fp, fp, fp, fp, fp, sp, sp, sp, sp, sp]
plotPiperackL2 = [fp, fp, sp, sp, sp, sp, sp, sp, fp, fp]
plotPiperackZ =  [ 0,  altopr,  altopr,  0,  altopr,  altopr,  0,  altopr, altopr,  0]

corEX = []
corEY = []
xa = []
ya =[]
za =[]
xa2 = []
ya2 =[]
za2 =[]
xa3 = []
ya3 =[]
za3 =[]
xa4 = []
ya4 =[]
za4 =[]
nivel =(altopr/seccionespr)



fig1= plt.figure(1)
plt.title('Visualización del Algoritmo Pathfinding')
plt.imshow(world)


def muestra2d(plotPiperackX,plotPiperackY,largo,ancho, corEX, corEY,xa,ya):
  plt.figure(2)
  plt.gca().invert_yaxis()
  plt.plot(plotPiperackX,plotPiperackY)
  plt.scatter(0,0, s=1, color='white')
  plt.scatter(largo,ancho,s=1, color='white')
  plt.scatter(corEX, corEY,s=20, marker = 'x', color='green')
  plt.scatter(xa,ya,s=20, color='blue')
  plt.title("Primer Nivel")
  plt.savefig('primer_nivel.png')


  return plt.plot

def muestra2d_2_nivel(plotPiperackX,plotPiperackY,largo,ancho, corEY, corEX,xa2,ya2):
  plt.figure(2)
  plt.gca().invert_yaxis()
  plt.plot(plotPiperackX,plotPiperackY)
  plt.scatter(0,0, s=1, color='white')
  plt.scatter(largo,ancho,s=1, color='white')
  plt.scatter(corEX, corEY,s=20, marker = 'x', color='green')
  plt.scatter(xa2,ya2,s=20, color='purple')
  plt.title("Segundo Nivel")
  plt.savefig('segundo_nivel.png')
  return plt.plot

def muestra2d_3_nivel(plotPiperackX,plotPiperackY,largo,ancho, corEY, corEX,xa3,ya3):
  plt.figure(3)
  plt.gca().invert_yaxis()
  plt.plot(plotPiperackX,plotPiperackY)
  plt.scatter(0,0, s=1, color='white')
  plt.scatter(largo,ancho,s=1, color='white')
  plt.scatter(corEX, corEY,s=20, marker = 'x', color='green')
  plt.scatter(xa3,ya3,s=20, color='purple')
  plt.title("Tercer Nivel")
  plt.savefig('tercer_nivel.png')
  return plt.plot

muestra2d(plotPiperackX,plotPiperackY,largo,ancho, corEY, corEX, xa, ya)

def muestraPiperack3d(seccionespr,plotPiperackX, plotPiperackY,plotPiperackL1, plotPiperackL2,plotPiperackZ,altopr,corEX, corEY,xa,ya,xa2,ya2, xa3,ya3, xa4,ya4,nivel):
  fig = plt.figure(figsize = (100,30))
  ax = fig.add_subplot(111, projection='3d')

  for i in range(seccionespr):
    ax.plot(plotPiperackX, plotPiperackY,((altopr/seccionespr))*(i+1), linewidth=10, color='red')

  ax.plot(plotPiperackL1, plotPiperackL2,plotPiperackZ, linewidth=10,color='red')
  ax.scatter3D(0, 0, 0,s = 1 , marker = "o", color='white')
  ax.scatter3D(largo, ancho, 0,s = 1 , marker = "o", color='white')
  ax.scatter3D(corEY, corEX, 0,s = 100 , marker = "x", color='green')
  ax.scatter3D(xa, ya, ((altopr/seccionespr)*1), s = 50, color='blue')
  ax.scatter3D(xa2, ya2, ((altopr/seccionespr)*2), s = 50, color='purple')
  ax.scatter3D(xa3, ya3, ((altopr/seccionespr)*3), s = 50, color='green')
  ax.scatter3D(xa4, ya4, ((altopr/seccionespr)*4), s = 50, color='yellow')
  ax.invert_xaxis()
  plt.title('Visualización 3D')
  plt.savefig('piperack3d.png')
  ax.view_init(30, 70)
 
  #ax.scatter3D(xp, yp, 2,s = 1000 , marker = "o", color='red')
  return plt.show()
muestraPiperack3d(seccionespr,plotPiperackX, plotPiperackY,plotPiperackL1, plotPiperackL2,plotPiperackZ,altopr,corEX, corEY,xa,ya,xa2,ya2, xa3,ya3, xa4,ya4,nivel)
 
all_paths_1_nivel = []
all_paths_2_nivel = []
all_paths_3_nivel = []

#ENTRADAS PREDETERMINADAS PARA MAYOR AGILIDAD EN LA ENTRADA DE LOS EQUIPOS

equipos = ["Bomba1", "Bomba2", "Tanque1", "Tanque2", "Reactor1", "Reactor2", "Fogón1", "Fogón2"]
tagEquipos = [1,2,  3,4,  5,6, 7,8]
corEX = [2, 10,  4, 4,   8, 1,   10, 6]
corEY = [0, 11,  0, 11,  0, 11,   0, 11]
corEZ = [0]*len(corEY)

'''
#CÓDIGO PARA DEFINIR LAS ENTRADAS DE LOS EQUIPOS DEL USUARIO -QUITAR COMILLAS SUPERIORES E INFERIORES PARA ACTIVAR

equipos = []
tagEquipos = []
corEX = []
corEY = []


ask = ''
while ask != "no":  #while submit new
  ask = input("¿Añadir un equipo?: ")
  if  ask != "no":
    nuevoEquipo = input("Ingrese nombre del equipo:\n")
    nuevoTag = input("Ingrese TAG de equipo:\n")
    nuevoCorEX = int(input("Ingrese coordenada en X:\n"))
    nuevoCorEY = int(input("Ingrese coordenada en Y:\n"))
    

    equipos.append(nuevoEquipo)
    tagEquipos.append(nuevoTag)
    corEX.append(nuevoCorEX)
    corEY.append(nuevoCorEY)
    
  
    print(equipos)
    print(tagEquipos)
    print(corEX)
    print(corEY)

    muestra2d(plotPiperackX,plotPiperackY,largo,ancho, corEY, corEX,xa, ya)
    
    muestraPiperack3d(seccionespr,plotPiperackX, plotPiperackY,plotPiperackL1, plotPiperackL2,plotPiperackZ,altopr,corEX, corEY,xa,ya,xa2,ya2, xa3,ya3, xa4,ya4,nivel)
 
'''
 
#generar una conexión

ask1 = ''
while ask1 != "no":  #while submit new
  ask = input("¿Añadir una conexión?: ")
  if ask == "no":
    break
  if  ask != "no":
    equipoInicial = int(input("Ingrese el número del equipo del equipo inicial: "))
    equipoFinal = int(input("Ingrese el número del equipo final: "))
    

    sx = corEX[equipoInicial-1]
    sy = corEY[equipoInicial-1]
    gx = corEX[equipoFinal-1]
    gy = corEY[equipoFinal-1]


        # define a start and end goals (x, y) (vertical, horizontal)

    start = (sx, sy)
    print(start)
    goal = (gx, gy)
    print(goal)
   
    
        #LLAMADA AL ALGORITMO A* PARA QUE ENCUENTRE LA MEJOR RUTA ENTRE DOS PUNTOS
    path = AStar(world).search(start, goal)
    
    if path is None:
      print("Genera Segundo Nivel")
                 
      lin_piperack_2 = []

      path2 = AStar(newWorld).search(start, goal)

      if path2 is None:
        print("Genera Tercer Nivel")
                    
        lin_piperack_3 = []

        path3 = AStar(newWorld2).search(start, goal)
            
        xs = [x[1] for x in path3]
        ys = [y[0] for y in path3]

        for z in range(len(xs)):
            newWorld2[ys[z]][xs[z]] = 1
            paths = (ys[z],xs[z])
            all_paths_3_nivel.append(paths)

        xa3= [x[1] for x in all_paths_3_nivel]
        ya3 = [y[0] for y in all_paths_3_nivel]
        za3 = [nivel*3]*len(ya3)

        plt.imshow(newWorld2)
        plt.title("Tercer Nivel A*")
        plt.plot
        

        muestra2d_3_nivel(plotPiperackX,plotPiperackY,largo,ancho, corEY, corEX,xa3,ya3)

        muestraPiperack3d(seccionespr,plotPiperackX, plotPiperackY,plotPiperackL1, plotPiperackL2,plotPiperackZ,altopr,corEX, corEY,xa,ya,xa2,ya2, xa3,ya3, xa4,ya4,nivel)
      
      else:
          
        xs = [x[1] for x in path2]
        ys = [y[0] for y in path2]
        zs = [nivel]*len(ys)

        for z in range(len(xs)):
            newWorld[ys[z]][xs[z]] = 1
            paths = (ys[z],xs[z])
            all_paths_2_nivel.append(paths)

        xa2= [x[1] for x in all_paths_2_nivel]
        ya2 = [y[0] for y in all_paths_2_nivel]
        za2 = [nivel*2]*len(ya2)

        plt.imshow(newWorld)
        plt.title("Segundo Nivel A*")
        plt.plot
        

        muestra2d_2_nivel(plotPiperackX,plotPiperackY,largo,ancho, corEX, corEY,xa2,ya2)

        muestraPiperack3d(seccionespr,plotPiperackX, plotPiperackY,plotPiperackL1, plotPiperackL2,plotPiperackZ,altopr,corEX, corEY,xa,ya,xa2,ya2, xa3,ya3, xa4,ya4,nivel)
        
    
    else:
      xs = [x[1] for x in path]
      ys = [y[0] for y in path]
      
      
      for z in range(len(xs)):
          world[ys[z]][xs[z]] = 1
          paths = (ys[z],xs[z])
          all_paths_1_nivel.append(paths)


      #guarda todos los valores de los paths
      
      
      xa= [x[1] for x in all_paths_1_nivel]
      ya = [y[0] for y in all_paths_1_nivel]
      za = [nivel]*len(ya)
      
      fig1=plt.figure(1)
      plt.imshow(world)
      plt.title("Primer Nivel A*")
      plt.plot

      muestra2d(plotPiperackX,plotPiperackY,largo,ancho, corEY, corEX,xa,ya)
      muestraPiperack3d(seccionespr,plotPiperackX, plotPiperackY,plotPiperackL1, plotPiperackL2,plotPiperackZ,altopr,corEX, corEY,xa,ya,xa2,ya2, xa3,ya3, xa4,ya4,nivel)


ask3 = ''
if ask3 != "no":  #while submit new
  ask = input("¿Desea un reporte Excel?: ")
  if  ask != "no":
    
   
    current_datetime = datetime.now(pytz.timezone("EST"))
    print('Reporte Excel Generado con Éxito '+str(current_datetime))

    workbook = xls.Workbook('reporte_MPL_.xlsx')

    worksheet = workbook.add_worksheet('hoja 1')
    worksheet.write(1,0,"REPORTE MAJOR PIPING LAYOUT - PAI G2C 2022-3 - UNAL -, fecha y hora:  "+str(current_datetime))

    worksheet.write(2,0,"AREA TOTAL LOTE")
    worksheet.write(3,0,"Largo")
    worksheet.write(4,0,"Ancho")
    worksheet.write(5,0,"AREA DEL PIPERACK")
    worksheet.write(6,0,"Largo")
    worksheet.write(7,0,"Ancho")
    worksheet.write(8,0,"EQUIPOS")
    worksheet.write(9,0,"Nombre")
    worksheet.write(10,0,"TAG")
    worksheet.write(11,0,"Coor. en x")
    worksheet.write(12,0,"Coor. en y")
    worksheet.write(13,0,"Coor. en z")


    worksheet2 = workbook.add_worksheet('hoja 2')
    worksheet2.write(1,0,"COORDENADAS DE LAS TUBERIAS POR NIVELES")
    worksheet2.write(2,0,"COORDENADAS DE LAS TUBERIAS 1 NIVEL")
    worksheet2.write(3,0,"Coor. en x")
    worksheet2.write(4,0,"Coor. en y")
    worksheet2.write(5,0,"Coor en z")
    worksheet2.write(6,0,"COORDENADAS DE LAS TUBERIAS 2 NIVEL")
    worksheet2.write(7,0,"Coor. en x")
    worksheet2.write(8,0,"Coor. en y")
    worksheet2.write(9,0,"Coor en z")
    worksheet2.write(10,0,"COORDENADAS DE LAS TUBERIAS 3 NIVEL")
    worksheet2.write(11,0,"Coor. en x")
    worksheet2.write(12,0,"Coor. en y")
    worksheet2.write(13,0,"Coor en z")

    worksheet.write(3, 1, largo)
    worksheet.write(4, 1, ancho)
    worksheet.write(6, 1, largopr)
    worksheet.write(7, 1, anchopr)

    for col_num, data in enumerate(equipos):
        worksheet.write(9, col_num+1, data)
    for col_num, data in enumerate(tagEquipos):
        worksheet.write(10, col_num+1, data)
    for col_num, data in enumerate(corEX):
        worksheet.write(11, col_num+1, data)
    for col_num, data in enumerate(corEY):
        worksheet.write(12, col_num+1, data)
    for col_num, data in enumerate(corEZ):
        worksheet.write(13, col_num+1, data)

    for col_num, data in enumerate(xa):
        worksheet2.write(3, col_num+1, data)
    for col_num, data in enumerate(ya):
        worksheet2.write(4, col_num+1, data)
    for col_num, data in enumerate(za):
        worksheet2.write(5, col_num+1, data)
    for col_num, data in enumerate(xa2):
        worksheet2.write(7, col_num+1, data)
    for col_num, data in enumerate(ya2):
        worksheet2.write(8, col_num+1, data)
    for col_num, data in enumerate(za2):
        worksheet2.write(9, col_num+1, data)
    for col_num, data in enumerate(xa3):
        worksheet2.write(11, col_num+1, data)
    for col_num, data in enumerate(ya3):
        worksheet2.write(12, col_num+1, data)
    for col_num, data in enumerate(za3):
        worksheet2.write(13, col_num+1, data)


    workbook.close()

ask4 = ''
if ask4 != "no":  #while submit new
  ask = input("¿Desea un reporte PDF?: ")
  if  ask != "no":        

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 2.5
    pdf.cell(40,10, 'REPORTE MAJOR PIPING LAYOUT - PAI 2C 2022-3')
    pdf.ln(10)
    current_datetime = datetime.now(pytz.timezone("EST"))
    pdf.cell(40,10, 'Generado: '+str(current_datetime))
    pdf.ln(10)

    pdf.cell(40,10, 'ÁREA DE TRABAJO')
    pdf.ln(5)
    pdf.cell(20,10,  'ANCHO')
    pdf.cell(20,10,  str(ancho))
    pdf.cell(20,10,  'LARGO')
    pdf.cell(20,10,  str(largo))
    pdf.ln(10)

    pdf.cell(40,10, 'PIPERACK')
    pdf.ln(5)
    pdf.cell(20,10,  'ANCHO')
    pdf.cell(20,10,  'LARGO')
    pdf.cell(20,10,  'ALTO')
    pdf.cell(20,10,  'SECCIONES')
    pdf.cell(20,10,  'ALTURA SECCIÓN')
    pdf.ln(5)
    pdf.cell(20,10,  str(anchopr))
    pdf.cell(20,10,  str(largopr))
    pdf.cell(20,10,  str(altopr))
    pdf.cell(20,10,  str(seccionespr))
    pdf.cell(20,10,  str(nivel))
    pdf.ln(10)


    pdf.cell(40,10, 'EQUIPOS')
    pdf.ln(5)
    for i in equipos:
      pdf.cell(20,10, i)
    pdf.ln(5)
    pdf.cell(40,10, 'TAG')
    pdf.ln(5)
    for j in tagEquipos:
      pdf.cell(20,10, str(j))
    pdf.ln(5)
    pdf.cell(40,10, 'COORDENADA X')
    pdf.ln(5)
    for k in corEX:
      pdf.cell(20,10, str(k))
    pdf.ln(5)
    pdf.cell(40,10, 'COORDENADA Y')
    pdf.ln(5)
    for l in corEY:
      pdf.cell(20,10, str(l))
    pdf.ln(5)
    pdf.cell(40,10, 'COORDENADA Z')
    pdf.ln(5)
    for n in corEZ:
      pdf.cell(20,10, str(n))



    pdf.ln(10)
    pdf.cell(40,10, 'IMAGENES NIVELES GENERADOS')
    pdf.ln(10)

    pdf.image('primer_nivel.png', x = None, y = None, w = 100, h = 100, type = '', link = '')
    pdf.ln(10)
    try:
      path2
    except:
      pdf.cell(40,10, 'VISUALIZACIÓN 3D')
      pdf.ln(10)
      pdf.image('piperack3d.png', x = None, y = None, w = 300, h = 300, type = '', link = '')
      pdf.ln(10)
      pdf.cell(40,10, 'MAJOR PIPING LAYOUT - PROYECTO PAI GRUPO 2C 2022-3 - UNIVERSIDAD NACIONAL DE COLOMBIA  - 3124005085')
      pdf.output('reporte_MPL.pdf', 'F')
    else:
      pdf.image('segundo_nivel.png', x = None, y = None, w = 100, h = 100, type = '', link = '')
      pdf.ln(10)
      try:
        path3
      except:      
        pdf.cell(40,10, 'VISUALIZACIÓN 3D')
        pdf.ln(10)
        pdf.image('piperack3d.png', x = None, y = None, w = 300, h = 300, type = '', link = '')
        pdf.ln(10)
        pdf.cell(40,10, 'MAJOR PIPING LAYOUT - PROYECTO PAI GRUPO 2C 2022-3 - UNIVERSIDAD NACIONAL DE COLOMBIA  - 3124005085')
        pdf.output('reporte_MPL.pdf', 'F')
      else:
        pdf.image('tercer_nivel.png', x = None, y = None, w = 100, h = 100, type = '', link = '')
        pdf.ln(10)
        pdf.cell(40,10, 'VISUALIZACIÓN 3D')
        pdf.ln(10)
        pdf.image('piperack3d.png', x = None, y = None, w = 300, h = 300, type = '', link = '')
        pdf.ln(10)
        pdf.cell(40,10, 'MAJOR PIPING LAYOUT - PROYECTO PAI GRUPO 2C 2022-3 - UNIVERSIDAD NACIONAL DE COLOMBIA  - 3124005085')
        pdf.output('reporte_MPL.pdf', 'F')
    pdf.output('reporte_MPL.pdf', 'F')
    print('Reporte PDF Generado con Éxito'+str(current_datetime))