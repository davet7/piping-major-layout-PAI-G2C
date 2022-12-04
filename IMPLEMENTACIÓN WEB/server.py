from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from form import PiperackArea, PiperackP, Equipos, Lineas # formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import os
from flask_caching import Cache
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



app = Flask(__name__)
app.config['SECRET_KEY'] = 'pai2C'



'''
@app.route("/")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
'''

#app.run(debug=True)

@app.route('/', methods=["POST", "GET"])
def index():
        return render_template('index.html')


def muestra2d(plotPiperackX,plotPiperackY,largo,ancho, corEX, corEY,xa,ya):
  fig2= plt.figure(2)
  plt.gca().invert_yaxis()
  plt.plot(plotPiperackX,plotPiperackY)
  plt.scatter(0,0, s=1, color='white')
  plt.scatter(largo,ancho,s=1, color='white')
  plt.scatter(corEX, corEY,s=20, marker = 'x', color='green')
  plt.scatter(xa,ya,s=20, color='blue')  


  return plt.savefig('static/area.png', bbox_inches='tight')

def muestraPiperack3d(seccionespr,plotPiperackX, plotPiperackY,plotPiperackL1, largo, ancho, plotPiperackL2,plotPiperackZ,altopr,corEX, corEY,xa,ya, nivel):
  fig = plt.figure(figsize = (100,30))
  ax = fig.add_subplot(111, projection='3d')

  for i in range(seccionespr):
    ax.plot(plotPiperackX, plotPiperackY,((altopr/seccionespr))*(i+1), linewidth=10, color='red')

  ax.plot(plotPiperackL1, plotPiperackL2,plotPiperackZ, linewidth=10,color='red')
  ax.scatter3D(0, 0, 0,s = 1 , marker = "o", color='white')
  ax.scatter3D(largo, ancho, 0,s = 1 , marker = "o", color='white')
  ax.scatter3D(corEX, corEY, 0,s = 200 , marker = "x", color='green')
  ax.scatter3D(xa, ya, ((altopr/seccionespr)*nivel), s = 100, color='blue')
  ax.view_init(30, 20)
 
  #ax.scatter3D(xp, yp, 2,s = 1000 , marker = "o", color='red')
  return plt.savefig('static/area3d.png', bbox_inches='tight')



@app.route('/app', methods=["POST", "GET"])
def appToda():
    form1=PiperackArea()
    form2=PiperackP()
    form4=Lineas()
    largo = None
    ancho = None
    world = None
    plotPiperackX =[]
    plotPiperackY =[]
    corEX=[]
    corEY=[]
    xa=[]
    ya=[]
    seccionespr=1
    plotPiperackL1 = []
    plotPiperackL2 = []
    plotPiperackZ = []
    altopr =1
    nivel=0
    anchoP = None
    largoP = None
    altoP = None
    seccionesP = None
    l = None
    fp = None
    sp=None

    
    if form2.is_submitted():
        ancho = int(request.form['ancho'])
        largo = int(request.form['largo'])
        anchoP =int(request.form['anchoP'])  
        largoP =int(request.form['largoP'])  
        altoP =int(request.form['altoP'])  
        seccionesP = int(request.form['seccionesP'])  

        world = np.zeros((largo,ancho))

             
        fp = int(((l - largoP)//2))  
        
        sp = int(l - ((l - largoP)//2)) 
        

        lin_piperack = []

        for i in range(fp):
            world[i][fp-1] = 5
            linea = (i,fp-1)
            lin_piperack.append(linea)
        for j in range(sp,l,1):  
            world[j][fp-1] = 5
            linea = (j,fp-1)
            lin_piperack.append(linea)
        for h in range(fp):
            world[h][sp] = 5
            linea = (h,sp)
            lin_piperack.append(linea)
        for k in range(sp,l,1):
            world[k][sp] = 5
            linea = (k, sp)
            lin_piperack.append(linea)
        for o in range(fp, sp+1, 1):
            world[fp-1][o] = 5
            linea = (fp-1, o)
            lin_piperack.append(linea)
        for p in range(fp, sp+1, 1):
            world[sp][p] = 5
            linea = (sp,p)
            lin_piperack.append(linea)

        xp = [x[1] for x in lin_piperack]
        yp = [y[0] for y in lin_piperack]

                      
        fig2= plt.figure(2)
        plt.gca().invert_yaxis()
        plt.plot(plotPiperackX,plotPiperackY)
        plt.scatter(0,0, s=1, color='white')
        plt.scatter(largo,ancho,s=1, color='white')
        plt.scatter(corEX, corEY,s=20, marker = 'x', color='green')
        plt.scatter(xa,ya,s=20, color='blue')
        plt.savefig('static/piperack2d.png', bbox_inches='tight')

        
        fig = plt.figure(figsize = (100,30))
        ax = fig.add_subplot(111, projection='3d')

        for i in range(seccionespr):
            ax.plot(plotPiperackX, plotPiperackY,((altopr/seccionespr))*(i+1), linewidth=10, color='red')

        ax.plot(plotPiperackL1, plotPiperackL2,plotPiperackZ, linewidth=10,color='red')
        ax.scatter3D(0, 0, 0,s = 1 , marker = "o", color='white')
        ax.scatter3D(largo, ancho, 0,s = 1 , marker = "o", color='white')
        ax.scatter3D(corEX, corEY, 0,s = 200 , marker = "x", color='green')
        ax.scatter3D(xa, ya, ((altopr/seccionespr)*nivel), s = 100, color='blue')
        ax.view_init(30, 20) 
        plt.savefig('static/piperack3d.png', bbox_inches='tight')       


        return render_template('app.html', form1=form1, form2=form2, form4=form4, largo=largo, ancho=ancho, anchoP=anchoP, largoP=largoP, altoP=altoP, seccionesP=seccionesP, get_plot = True, plot_urlpr = 'static/piperack2d.png', plot3d_urlpr= 'static/piperack3d.png')
    
  

    if form2.is_submitted():
        anchoP =int(request.form['anchoP'])  
        largoP =int(request.form['largoP'])  
        altoP =int(request.form['altoP'])  
        seccionesP = int(request.form['seccionesP'])  

        world = np.zeros((largo,ancho))

             
        fp = int(((l - largoP)//2))  
        
        sp = int(l - ((l - largoP)//2)) 
        

        lin_piperack = []

        for i in range(fp):
            world[i][fp-1] = 5
            linea = (i,fp-1)
            lin_piperack.append(linea)
        for j in range(sp,l,1):  
            world[j][fp-1] = 5
            linea = (j,fp-1)
            lin_piperack.append(linea)
        for h in range(fp):
            world[h][sp] = 5
            linea = (h,sp)
            lin_piperack.append(linea)
        for k in range(sp,l,1):
            world[k][sp] = 5
            linea = (k, sp)
            lin_piperack.append(linea)
        for o in range(fp, sp+1, 1):
            world[fp-1][o] = 5
            linea = (fp-1, o)
            lin_piperack.append(linea)
        for p in range(fp, sp+1, 1):
            world[sp][p] = 5
            linea = (sp,p)
            lin_piperack.append(linea)

        xp = [x[1] for x in lin_piperack]
        yp = [y[0] for y in lin_piperack]

                      
        fig2= plt.figure(2)
        plt.gca().invert_yaxis()
        plt.plot(plotPiperackX,plotPiperackY)
        plt.scatter(0,0, s=1, color='white')
        plt.scatter(largo,ancho,s=1, color='white')
        plt.scatter(corEX, corEY,s=20, marker = 'x', color='green')
        plt.scatter(xa,ya,s=20, color='blue')
        plt.savefig('static/piperack2d.png', bbox_inches='tight')

        
        fig = plt.figure(figsize = (100,30))
        ax = fig.add_subplot(111, projection='3d')

        for i in range(seccionespr):
            ax.plot(plotPiperackX, plotPiperackY,((altopr/seccionespr))*(i+1), linewidth=10, color='red')

        ax.plot(plotPiperackL1, plotPiperackL2,plotPiperackZ, linewidth=10,color='red')
        ax.scatter3D(0, 0, 0,s = 1 , marker = "o", color='white')
        ax.scatter3D(largo, ancho, 0,s = 1 , marker = "o", color='white')
        ax.scatter3D(corEX, corEY, 0,s = 200 , marker = "x", color='green')
        ax.scatter3D(xa, ya, ((altopr/seccionespr)*nivel), s = 100, color='blue')
        ax.view_init(30, 20) 
        plt.savefig('static/piperack3d.png', bbox_inches='tight')       


        return render_template('app.html', form1=form1, form2=form2, form4=form4, anchoP=anchoP, largoP=largoP, altoP=altoP, seccionesP=seccionesP, get_plot = True, plot_urlpr = 'static/piperack2d.png', plot3d_urlpr= 'static/piperack3d.png')
    
    return render_template('app.html', form1=form1, form2=form2, form4=form4)




@app.route('/planta', methods = ['GET', 'POST'])
def planta():
    form=PiperackArea()
    largo = None
    ancho = None
    world = None
    f= None
    l = None
    fp = None
    sp=None
    if form.is_submitted():
        ancho = int(request.form['ancho'])
        largo = int(request.form['largo'])
        world = np.zeros((largo,ancho))

        fig1 = plt.figure()
        plt.imshow(world)              
        plt.savefig('static/area.png', bbox_inches='tight')

        fig2 = plt.figure(figsize = (100,30))    
        ax = fig2.add_subplot(111, projection='3d')
        ax.scatter3D(largo, ancho, 2,s = 1000 , marker = "o", color='red')
        ax.scatter3D(0, ancho, 2,s = 1000 , marker = "o", color='red')
        ax.scatter3D(largo, 0, 2,s = 1000 , marker = "o", color='red')
        ax.scatter3D(0, 0, 2,s = 1000 , marker = "o", color='red')
        plt.savefig('static/area3d.png', bbox_inches='tight')
       


        return render_template('planta.html', form=form, largo=largo, ancho=ancho, get_plot = True, plot_url = 'static/area.png', plot3d_url= 'static/area3d.png')
    return  render_template('planta.html', form=form)



        

@app.route('/piperack', methods = ['GET', 'POST'])
def piperack():
    form=PiperackP()
    largo = None
    ancho = None
    world = None
    plotPiperackX =[]
    plotPiperackY =[]
    corEX=[]
    corEY=[]
    xa=[]
    ya=[]
    seccionespr=1
    plotPiperackL1 = []
    plotPiperackL2 = []
    plotPiperackZ = []
    altopr =1
    nivel=0
    anchoP = 0
    largoP = 0
    altoP = 0
    seccionesP = 0
    l = 0
    fp = 0
    sp=0
    

    
    if form.is_submitted():
        ancho = int(request.form['ancho'])
        largo = int(request.form['largo'])
        anchoP =int(request.form['anchoP'])  
        largoP =int(request.form['largoP'])  
        altoP =int(request.form['altoP'])  
        seccionesP = int(request.form['seccionesP'])  

        seccionespr += 1

        world = np.zeros((largo,ancho))
        l = int(len(world))
        
        fp = int(((l - largoP)//2))  
        
        sp = int(l - ((l - largoP)//2)) 
        

        lin_piperack = []

        for i in range(fp):
            world[i][fp-1] = 5
            linea = (i,fp-1)
            lin_piperack.append(linea)
        for j in range(sp,l,1):  
            world[j][fp-1] = 5
            linea = (j,fp-1)
            lin_piperack.append(linea)
        for h in range(fp):
            world[h][sp] = 5
            linea = (h,sp)
            lin_piperack.append(linea)
        for k in range(sp,l,1):
            world[k][sp] = 5
            linea = (k, sp)
            lin_piperack.append(linea)
        for o in range(fp, sp+1, 1):
            world[fp-1][o] = 5
            linea = (fp-1, o)
            lin_piperack.append(linea)
        for p in range(fp, sp+1, 1):
            world[sp][p] = 5
            linea = (sp,p)
            lin_piperack.append(linea)

        xp = [x[1] for x in lin_piperack]
        yp = [y[0] for y in lin_piperack]
                
        plotPiperackX = [fp, fp, sp, sp, fp]
        plotPiperackY = [fp, sp, sp, fp, fp]

        plotPiperackL1 = [fp, fp, fp, fp, fp, sp, sp, sp, sp, sp]
        plotPiperackL2 = [fp, fp, sp, sp, sp, sp, sp, sp, fp, fp]
        plotPiperackZ =  [ 0,  altopr,  altopr,  0,  altopr,  altopr,  0,  altopr, altopr,  0]

        
        
        fig2= plt.figure(2)
        plt.gca().invert_yaxis()
        plt.plot(plotPiperackX,plotPiperackY)
        plt.scatter(0,0, s=1, color='white')
        plt.scatter(largo,ancho,s=1, color='white')
        plt.scatter(corEX, corEY,s=20, marker = 'x', color='green')
        plt.scatter(xa,ya,s=20, color='blue')           
        plt.savefig('static/piperack2d.png', bbox_inches='tight')

        fig = plt.figure(figsize = (100,30))
        ax = fig.add_subplot(111, projection='3d')

        for i in range(seccionespr):
            ax.plot(plotPiperackX, plotPiperackY,((altopr/seccionespr))*(i+1), linewidth=10, color='red')

        ax.plot(plotPiperackL1, plotPiperackL2,plotPiperackZ, linewidth=10,color='red')
        ax.scatter3D(0, 0, 0,s = 1 , marker = "o", color='white')
        ax.scatter3D(largo, ancho, 0,s = 1 , marker = "o", color='white')
        ax.scatter3D(corEX, corEY, 0,s = 200 , marker = "x", color='green')
        ax.scatter3D(xa, ya, ((altopr/seccionespr)*nivel), s = 100, color='blue')
        ax.view_init(30, 20)
        plt.savefig('static/piperack3d.png', bbox_inches='tight')

        return render_template('piperack.html', form=form, largo = largo, ancho = ancho, anchoP=anchoP, largoP=largoP, altoP=altoP, seccionesP=seccionesP, get_plot = True, plot_urlpr = 'static/piperack2d.png', plot3d_urlpr= 'static/piperack3d.png')
    return  render_template('piperack.html',form=form)

@app.route('/equipos')
def equipos():
    return  render_template('equipos.html')



@app.route('/lineas')
def lineas():
    form=Lineas()
    return  render_template('lineas.html', form=form)

@app.route('/resultados')
def resultados():
    return  render_template('resultados.html')


@app.route('/blog')
def blog():
    posts =[{'title': 'EL Tachudita', 'author': 'Tichis'},
            {'title': 'EL Jruss', 'author': 'Russ'}]
    return  render_template('index.html', autor ='Tichis', sunny= False, posts = posts)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = PiperackArea()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('signUp.html', form=form, result=result)    

@app.route('/blog/<string:blog_id>')
def blogpost(blog_id):
    
    return 'This is the blog' + blog_id

if __name__ == '__main__':
    app.run()

