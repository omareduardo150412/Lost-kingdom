# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 01:31:48 2020

@author: omar_
"""

import pygame as pg 
pg.init()#inicializamos
ancho=1050#750
alto=600
##colores en RGB
gris=(220,220,220)
azul=(0,0,255)
gris_c=(248,248,255)
verde=(0,128,0)
cafe=(139,69,19)
sand=(255,255,0)
rojo=(255,0,0)
snow=(255,250,250)
claro_v=(255,234,128)
negro=(0,0,0)
tierra = pg.image.load("tierra.jpg")
mon = pg.image.load("muro.jpg")
marco= pg.image.load("marco.jpg")
personaje=pg.image.load("caballero.png")
pg.mixer.music.load("musica_fondo.mp3")
Font = pg.font.SysFont("Arial",25)
valores_c=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
posiciones=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
coordena=list(zip(posiciones,valores_c))
mapa=[]

class InputBox:

    def __init__(self, x, y, w, h,t,font,text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = gris
        self.text = text
        self.txt_surface = Font.render(text, True, self.color)
        self.active = False
        self.int=t
        self.string=''
        self.fuente=Font
        self.prioridad="a,d,b,i"
        self.camino=list()
        self.successful=False
        self.error=False
        self.coordenadaI=[]
        self.coordenadaF=[]
        
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = snow if self.active else gris
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if self.int == 1:
                        coor=filtro_input(self.text) #['10','a'] <----'(10,a)'
                        self.string=get_type(mapa,coor)
                    if self.int == 2:
                        texto_intput=self.text.split('->')
                        point_clean=filtro_input(texto_intput[0])
                        tipo_c=texto_intput[1]
                        tipo_clean=tipo_c.lower()
                        if tipo_clean == 'muro' or tipo_clean == 'paso':  
                              change_type(mapa,point_clean,tipo_clean)
                    if self.int == 3:
                        texto_intput=self.text.split('->')  # 10,a>>2,0  ['10,a','2,0']
                        pi=filtro_input(texto_intput[0])
                        pf=filtro_input(texto_intput[1])
                        validar_pi=validar_pos(mapa,pi)
                        validar_pf=validar_pos(mapa,pf)
                        if validar_pi == True and validar_pf == True:
                            priority=self.prioridad.split(',')
                            self.coordenadaI=pi
                            self.coordenadaF=pf
                            self.camino=profundidad(mapa,pi,pf,priority)
                            self.successful=True
                        else:
                            self.error=True
                    if self.int == 4:
                        self.prioridad=self.text.lower()
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.fuente.render(self.text, True,negro)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)#, 2)
        screen.blit(self.txt_surface, (self.rect.x+3, self.rect.y+3))
    def draw_text(self,screen,x,y,tam):
        mostrar_texto(screen,"Ravie",tam,self.string,x,y,claro_v)
        
class decision:
    def __init__(self,f, x, y,veces=0):
        self.pos=f
        self.px=x
        self.py=y
        self.pasado=veces
        self.decision=''
        
class coordena_m:
    def __init__(self,valor,activado,pasos=0):
        self.visitado=activado
        self.tipo=valor
        self.paso=pasos
        self.acciones=[]
        self.ver=False
        
##################################  fin de las clases ############################
def validar_pos(mapa,pxy): 
    flag=False
    px=0
    py=int(pxy[0]) 
    py_m=py-1
    if (py < 16) and (pxy[1]<'p'):
        for p in range(len(coordena)):
           puntos=coordena[p]
           if puntos[1] == pxy[1]:
               px=puntos[0]
               p=15
        for pmy in range(len(mapa)):
            fila=mapa[pmy]
            for pmx in range(len(fila)):
                if pmy == py_m and pmx ==px:
                   punto=fila[pmx]
                   if punto.tipo== 1:
                       flag=True
                   pmx=15
                   pmy=15
    else:
        flag=False
    return flag
def coordenas_mapa(punto):
    ind=17
    valores_c=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    posiciones=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    coordenada=list(zip(posiciones,valores_c))
    px=punto[1]
    coord=[]
    coord.append(int(punto[0])-1)
    for letra in coordenada:
        if px == letra[1]:
            ind=letra[0]
            coord.append(ind)
    if ind == 17:
        coord.append(0)
    return coord


def _mover_(mapa,px,py,p,caso):
    aux=decision(False,px,py)
    if p == 'b' and (caso ==1 or caso ==2 or caso==6 or caso== 7 or caso == 8 or caso==9):
        fila=mapa[py+1]
        punto=fila[px]
        
        if punto.tipo == 1:
            aux.py=py+1
            aux.decision='b'
            aux.pos=True
            punto.visitado=True
            punto.paso=punto.paso+1
            aux.pasado=punto.paso
        else:
            aux.pos = False
    elif p == 'a' and (caso ==2 or caso==3 or caso == 4 or caso ==5 or caso ==6 or caso==9):
        fila=mapa[py-1]
        punto=fila[px]
        if punto.tipo == 1 :
            aux.py=py-1
            aux.decision='a'
            aux.pos=True
            punto.visitado=True
            punto.paso=punto.paso+1
            aux.pasado=punto.paso
        else:
            aux.pos = False   
    elif p == 'd' and (caso ==1 or caso==2 or caso == 3 or caso ==4 or caso ==8 or caso==9):
        fila=mapa[py]
        punto=fila[px+1]
        if punto.tipo == 1:
            aux.px=px+1
            aux.pos=True
            punto.visitado=True
            punto.paso=punto.paso+1
            aux.decision='d'
            aux.pasado=punto.paso
        else:
            aux.pos = False   
    elif p == 'i' and (caso ==4 or caso==5 or caso == 6 or caso ==7 or caso ==8 or caso==9):
        fila=mapa[py]
        punto=fila[px-1]
        if punto.tipo == 1:
            aux.px=px-1
            aux.pos=True
            punto.visitado=True
            aux.decision='i'
            punto.paso=punto.paso+1
            aux.pasado=punto.paso
        else:
            aux.pos= False 
    #print(px+""+py)
    return aux

def comparar(p1,p2):
    b1=False
    if p1[0]==p2[0] and p1[1]==p2[1]:
        b1=True
    return b1
def diferentes_pos(py,px):
    aux_ind=0
    if py == 0 and px ==0:
        aux_ind=1
    elif (py>0 and py<14)and px==0:
        aux_ind=2
    elif py==14 and px==0:
        aux_ind=3
    elif py==14 and (px>0 and px<14):
        aux_ind=4
    elif py==14 and px==14:
        aux_ind=5
    elif(py>0 and py<14)and px==14:
        aux_ind=6
    elif py==0 and px==14:
        aux_ind=7
    elif py==0 and (px>0 and px<14):
        aux_ind=8
    else:
        aux_ind=9
   # print(aux_ind)
    return aux_ind
def cambioDL(px):
    valores_c=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    posiciones=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    coordenada=list(zip(posiciones,valores_c))
    letra=''
    for letras in coordenada:
        if px == letras[0]:
            letra=letras[1]
    return letra

def un_solo_camino(valor, mapa,px,py):
    aux=decision(False,px,py)  ## caso |
    if valor == 2 or valor == 9 or valor == 6:
        fila_arriba=mapa[py-1]
        punto_arriba=fila_arriba[px]
        fila_abajo=mapa[py+1]
        punto_abajo=fila_abajo[px]
        if punto_arriba.paso >= 1 and punto_abajo.paso == 0 and punto_arriba.tipo == 1 and punto_abajo.tipo == 1:
            aux.py=py+1
            aux.pos=True
            punto_abajo.visitado=True
            punto_abajo.paso=punto_abajo.paso+1
            aux.decision='b'
            aux.pasado=punto_abajo.paso
        if  punto_arriba.paso == 0 and punto_abajo.paso >= 1 and punto_arriba.tipo == 1 and punto_abajo.tipo == 1:
            aux.py=py-1
            aux.pos=True
            punto_arriba.visitado=True
            aux.decision='a'
            punto_arriba.paso=punto_arriba.paso+1
            aux.pasado=punto_arriba.paso
    if valor == 8 or valor == 9 or valor == 4: ##caso --
        fila_v=mapa[py]
        punto_d=fila_v[px+1]
        punto_i=fila_v[px-1]
        if punto_d.paso>=1 and punto_i.paso ==0 and punto_d.tipo==1 and punto_i.tipo ==1 :
            aux.px=px-1
            aux.pos=True
            punto_i.visitado=True
            aux.decision='i'
            punto_i.paso=punto_i.paso+1
            aux.pasado=punto_i.paso
        if punto_d.paso==0 and punto_i.paso >=1 and punto_d.tipo==1 and punto_i.tipo ==1:
            aux.px=px+1
            aux.pos=True
            punto_d.visitado=True
            punto_d.paso=punto_d.paso+1
            aux.decision='d'
            aux.pasado=punto_d.paso
    if valor == 1 or valor == 2 or valor == 8 or valor == 9:
        fila_v=mapa[py+1]
        punto_abajo=fila_v[px]
        fila_v=mapa[py]
        punto_d=fila_v[px+1]
        if punto_d.paso>=1 and punto_abajo.paso==0 and punto_d.tipo==1 and punto_abajo.tipo ==1:
           aux.py=py+1
           aux.pos=True
           punto_abajo.visitado=True
           aux.decision='b'
           punto_abajo.paso=punto_abajo.paso+1
           aux.pasado=punto_abajo.paso 
        if punto_d.paso==0 and punto_abajo.paso>=1 and punto_d.tipo==1 and punto_abajo.tipo ==1:
            aux.px=px+1
            aux.pos=True
            punto_d.visitado=True
            aux.decision='d'
            punto_d.paso=punto_d.paso+1
            aux.pasado=punto_d.paso
    if valor == 6 or valor == 7 or valor == 8 or valor == 9:  
        fila_v=mapa[py+1]
        punto_abajo=fila_v[px]
        fila_v=mapa[py]
        punto_i=fila_v[px-1]
        if punto_i.paso>=1 and punto_abajo.paso==0 and punto_i.tipo==1 and punto_abajo.tipo ==1:
           aux.py=py+1
           aux.pos=True
           punto_abajo.visitado=True
           aux.decision='b'
           punto_abajo.paso=punto_abajo.paso+1
           aux.pasado=punto_abajo.paso 
        if punto_i.paso==0 and punto_abajo.paso>=1 and punto_i.tipo==1 and punto_abajo.tipo ==1:
            aux.px=px-1
            aux.pos=True
            punto_i.visitado=True
            aux.decision='i'
            punto_i.paso=punto_i.paso+1
            aux.pasado=punto_i.paso
    if valor == 4 or valor == 9 or valor == 5 or valor == 6:
        fila_v=mapa[py-1]
        punto_arriba=fila_v[px]
        fila_v=mapa[py]
        punto_i=fila_v[px-1]
        if punto_i.paso>=1 and punto_arriba.paso==0 and punto_i.tipo==1 and punto_arriba.tipo ==1:
            aux.py=py-1
            aux.pos=True
            punto_arriba.visitado=True
            aux.decision='a'
            punto_arriba.paso=punto_arriba.paso+1
            aux.pasado=punto_arriba.paso
        if punto_i.paso==0 and punto_arriba.paso>=1 and punto_i.tipo==1 and punto_arriba.tipo ==1:
            aux.px=px-1
            aux.pos=True
            punto_i.visitado=True
            aux.decision='i'
            punto_i.paso=punto_i.paso+1
            aux.pasado=punto_i.paso
    if valor == 2 or valor == 9 or valor == 3 or valor == 4:
        fila_v=mapa[py-1]
        punto_arriba=fila_v[px]
        fila_v=mapa[py]
        punto_d=fila_v[px+1]
        if punto_d.paso>=1 and punto_arriba.paso==0 and punto_d.tipo==1 and punto_arriba.tipo ==1:
            aux.py=py-1
            aux.pos=True
            punto_arriba.visitado=True
            punto_arriba.paso=punto_arriba.paso+1
            aux.decision='a'
            aux.pasado=punto_arriba.paso
        if punto_d.paso==0 and punto_arriba.paso>=1 and punto_d.tipo==1 and punto_arriba.tipo ==1:
            aux.px=px+1
            aux.pos=True
            punto_d.visitado=True
            aux.decision='d'
            punto_d.paso=punto_d.paso+1
            aux.pasado=punto_d.paso
    return aux

def _validar_pos_(valor, mapa,px,py):
    detector=False
   # __escondido__=False
    #__visitado__=False
    lista_tipo=[]
    visitados=0
    if valor == 1:
        lista_tipo.append(_checar_punto_(mapa,px,py,'d',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'b',valor))
    if valor == 2:
        lista_tipo.append(_checar_punto_(mapa,px,py,'d',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'b',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'a',valor))
    if valor == 3:
        lista_tipo.append(_checar_punto_(mapa,px,py,'a',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'d',valor))
    if valor == 4:
        lista_tipo.append(_checar_punto_(mapa,px,py,'d',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'i',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'a',valor))
    if valor == 5:
        lista_tipo.append(_checar_punto_(mapa,px,py,'a',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'i',valor))
    if valor == 6:
        lista_tipo.append(_checar_punto_(mapa,px,py,'i',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'b',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'a',valor))
    if valor == 7:
        lista_tipo.append(_checar_punto_(mapa,px,py,'i',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'b',valor))
    if valor == 8:
        lista_tipo.append(_checar_punto_(mapa,px,py,'d',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'b',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'i',valor))
    if valor == 9:
        lista_tipo.append(_checar_punto_(mapa,px,py,'i',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'b',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'a',valor))
        lista_tipo.append(_checar_punto_(mapa,px,py,'d',valor))
    for bloque in lista_tipo:
        if bloque[0] == 1:
            visitados+=1
            
    if visitados==2:
        detector=True
    else:
        detector=False
        
    return detector


def _checar_punto_(mapa,px,py,p,caso):
    valores_punto=[]
    if p == 'b' and (caso ==1 or caso ==2 or caso==6 or caso== 7 or caso == 8 or caso==9):
        fila=mapa[py+1]
        punto=fila[px]
        valores_punto.append(punto.tipo)
        valores_punto.append(punto.paso)
    elif p == 'a' and (caso ==2 or caso==3 or caso == 4 or caso ==5 or caso ==6 or caso==9):
        fila=mapa[py-1]
        punto=fila[px]
        valores_punto.append(punto.tipo)
        valores_punto.append(punto.paso)
    elif p == 'd' and (caso ==1 or caso==2 or caso == 3 or caso ==4 or caso ==8 or caso==9):
        fila=mapa[py]
        punto=fila[px+1]
        valores_punto.append(punto.tipo)
        valores_punto.append(punto.paso)
    elif p == 'i' and (caso ==4 or caso==5 or caso == 6 or caso ==7 or caso ==8 or caso==9):
        fila=mapa[py]
        punto=fila[px-1]
        valores_punto.append(punto.tipo)
        valores_punto.append(punto.paso)
    else:
        valores_punto.append(0)
        valores_punto.append(0)
    return valores_punto

def lugares_visitados(mapa,px,py,p_aux):
    flag_place=True
    fila_lug=mapa[py]
    punto_vis=fila_lug[px]
    #print(punto_vis.acciones)
    for accion in punto_vis.acciones:
        if accion == p_aux:
            flag_place=False
    return flag_place
    
    

def profundidad(mapa,pi,pf,prioridad):
    p1=coordenas_mapa(pi)
    p2=coordenas_mapa(pf)
    ruta=[]
    puntos=[]
    py=p1[0]
    px=p1[1]
    p=0
    bandera=True 
    fila_=mapa[py]
    point=fila_[px]
    point.visitado=True
    point.paso=1
    ruta.append(str(py+1)+ cambioDL(px))
    however=True
    while bandera:
        aux=diferentes_pos(py,px)
        camino_1=_validar_pos_(aux, mapa,px,py) 
        if camino_1== True:
           # print("pasos:"+str(px)+" "+str(py))
            however=False
            res=un_solo_camino(aux, mapa,px,py)
            if res.pos == True:
                however=False
                res.pos=False
                _fila_=mapa[py]
                _punto_=_fila_[px]
                _punto_.acciones.append(res.decision)
                puntos.append([res.py,res.px])
                ruta.append(str(res.py+1)+ cambioDL(res.px))
                if comparar(p2,[res.py,res.px]) == True:
                    bandera=False
                else:
                    bandera=True
                    px=res.px
                    py=res.py
                    if res.pasado == 5:
                          bandera=False
            else: 
                however=True
        else:
            however == True
        if however == True:
            
            while p<len(prioridad):
                ###
                if lugares_visitados(mapa,px,py,prioridad[p]) == True:
                    res=_mover_(mapa,px,py,prioridad[p],aux)
                    if res.pos == True:
                            _fila_=mapa[py]
                            _punto_=_fila_[px]
                            _punto_.acciones.append(res.decision)
                            #print(res.decision)
                            p=4
                            res.pos=False
                            #print(str(res.py+1)+ cambioDL(res.px))
                            puntos.append([res.py,res.px])
                            ruta.append(str(res.py+1)+ cambioDL(res.px))
                            if comparar(p2,[res.py,res.px]) == True:
                                bandera=False
                            else:
                                
                                bandera=True
                                px=res.px
                                py=res.py
                                if res.pasado == 5:
                                      bandera=False
                       
                p+=1
            p=0
    
        however=True
       # print(str(py)+"   x="+str(px))
    #print(puntos)
    #print('->'.join(ruta))
    puntos_final=list(zip(ruta,puntos))    
    return puntos_final


def limpiar_mapa(mapa):
    for fila in mapa:
        for punto in fila:
            punto.visitado=False
            punto.paso=0
            punto.acciones=[]


###################################fin del algoritmo de profundidad###############
def dibujar_muro(superficie,rectangulo,color,mostrar):
    
    if mostrar == True:
        if color == 0:    
            #pygame.draw.rect(superficie,gris, rectangulo)
            picture = pg.transform.scale(mon, [50, 40])
            superficie.blit(picture,rectangulo)
        if color ==1:
            #pygame.draw.rect(superficie,cafe, rectangulo)
            picture = pg.transform.scale(tierra, [50, 40])
            superficie.blit(picture,rectangulo)
    else:
        pg.draw.rect(superficie,negro,[rectangulo[0],rectangulo[1],50,40])
        

def dibujar_muro_mos(superficie,rectangulo,color):
    
        if color == 0:    
            #pygame.draw.rect(superficie,gris, rectangulo)
            picture = pg.transform.scale(mon, [50, 40])
            superficie.blit(picture,rectangulo)
        if color ==1:
            #pygame.draw.rect(superficie,cafe, rectangulo)
            picture = pg.transform.scale(tierra, [50, 40])
            superficie.blit(picture,rectangulo)
   
        
      
    
def construir_mapa(mapa):
    muros = []
    color =[]
    visitado=[]
    x = 0
    y = 0
    for fila in mapa:
          for punto in fila:
              muros.append([x,y])
              color.append(punto.tipo)
              visitado.append(punto.ver)
              x+=50
          x=0
          y+=40
    
    muros_color=list(zip(muros,color,visitado))
    return muros_color

def dibujar(superficie,mapa_muros,ver):
    if ver == True:
        for muro in mapa_muros:
            dibujar_muro(superficie,muro[0],muro[1],muro[2])
    else:
        for muro in mapa_muros:
            dibujar_muro_mos(superficie,muro[0],muro[1])
            
def read_text(ruta):
    doc_top=open(ruta,'r',encoding="utf-8").read()
    return doc_top   
#mapas
def get_labyrinth(filas_laberinto):
    laberinto=[]
    for fila in filas_laberinto:
        if fila != '':
            columnas=fila.split(',')
            fila_valores=[]
            for punto in columnas:
                fila_valores.append(coordena_m(int(punto),False))
            laberinto.append(fila_valores)
    return laberinto


def values(num):
    _aux_=''
    if num == 0:
        _aux_='Muro'
    elif num == 1:
        _aux_='Paso'
    return _aux_

def change_types(tipo):
    num=0
    if tipo == 'muro':
        num=0
    elif tipo == 'paso':
        num=1
    return num

def get_type(mapa,pxy):
    px=0
    tipo_celda=''
    py=int(pxy[0]) 
    py_m=py-1
    p=0
    if (py < 16) and (pxy[1]<'p'):
        while p <len(coordena):
           puntos=coordena[p]
           if puntos[1] == pxy[1]:
               px=puntos[0]
               p=15
           p+=1
        fila=mapa[py_m]
        tipo_celda=values(fila[px].tipo)
    else:
       tipo_celda="Muro"
    return tipo_celda

def change_type(mapa,pxy,tipo):
    px=0
    py=int(pxy[0]) 
    py_m=py-1
    p=0
    if (py < 16) and (pxy[1]<'p'):
        while p <len(coordena):
           puntos=coordena[p]
           if puntos[1] == pxy[1]:
               px=puntos[0]
               p=15
           p+=1
        fila=mapa[py_m]
        fila[px].tipo=change_types(tipo)


def filtro_input(cadena):
    cadena_min=cadena.lower()
    cadena_clean=cadena_min.lstrip('(')
    cadena_final=cadena_clean.rstrip(')')
    #print(cadena_final[1])
    tokens=[]
    obtener=0
    for pos_a in cadena_final:
        if pos_a == ',':
            obtener=1
        if pos_a == '.':
            obtener=2
    if obtener  == 1:
       tokens=cadena_final.split(',')
    if obtener == 2:
       tokens=cadena_final.split('.')
    if obtener == 0:
      if cadena_final[-1] >='a' and cadena_final[-1]<'p':
         coor=cadena_final.split(cadena_final[-1])
         tokens.append(coor[0])
         tokens.append(cadena_final[-1])
      else:
         coor=cadena_final.split(cadena_final[-1])
         tokens.append(coor[0])
         tokens.append('r')
    return tokens
    
def mostrar_texto(ventana,fuente_text,tam, texto,x,y,color):
    fuente=pg.font.SysFont(fuente_text,tam)
    texto_v=fuente.render(texto,True,color)
    ventana.blit(texto_v,[x,y])

def cargar_sonidos():
    songs=[]
    songs.append(pg.mixer.Sound('Sonidos/ready.wav'))
    songs.append(pg.mixer.Sound('Sonidos/winner.wav'))
    songs.append(pg.mixer.Sound('Sonidos/warning.mp3'))
    return songs

def mostrar_laberinto_pasos(valor, mapa,px,py):
    casos_mostar(px, py,'c',mapa)
    if valor == 1:
        casos_mostar(px, py,'b',mapa)
        casos_mostar(px, py,'d',mapa)
    elif valor == 2:
        casos_mostar(px, py,'b',mapa)
        casos_mostar(px, py,'d',mapa)
        casos_mostar(px, py,'a',mapa)
    elif valor == 3:
        casos_mostar(px, py,'a',mapa)
        casos_mostar(px, py,'d',mapa)
    elif valor == 4:
        casos_mostar(px, py,'i',mapa)
        casos_mostar(px, py,'d',mapa)
        casos_mostar(px, py,'a',mapa) 
    elif valor == 5:
        casos_mostar(px, py,'a',mapa)
        casos_mostar(px, py,'i',mapa)
    elif valor == 6:
        casos_mostar(px, py,'a',mapa)
        casos_mostar(px, py,'i',mapa)
        casos_mostar(px, py,'b',mapa)
    elif valor == 7:
        casos_mostar(px, py,'b',mapa)
        casos_mostar(px, py,'i',mapa)
    elif valor == 8:
        casos_mostar(px, py,'d',mapa)
        casos_mostar(px, py,'i',mapa)
        casos_mostar(px, py,'b',mapa)
    elif valor == 9:
        casos_mostar(px, py,'d',mapa)
        casos_mostar(px, py,'i',mapa)
        casos_mostar(px, py,'b',mapa)
        casos_mostar(px, py,'a',mapa)

        
def casos_mostar(px, py, accion,mapa):
    if accion == 'c':
       fila=mapa[py]
       punto_f=fila[px]
       punto_f.ver=True
    elif accion == 'a':
       fila=mapa[py-1]
       punto_f=fila[px]
       punto_f.ver=True
    elif accion  == 'd':
       fila=mapa[py]
       punto_f=fila[px+1]
       punto_f.ver=True 
    elif accion == 'i':
       fila=mapa[py]
       punto_f=fila[px-1]
       punto_f.ver=True
    elif accion == 'b':
       fila=mapa[py+1]
       punto_f=fila[px]
       punto_f.ver=True
     
if __name__ == '__main__':

    matriz_laberinto= read_text('labyrinth.txt')
    filas_laberinto=matriz_laberinto.split('\n')
    mapa_valores=get_labyrinth(filas_laberinto)
    mapa=mapa_valores
    ventana = pg.display.set_mode((ancho,alto))
    pg.display.set_caption("Lost Kingdom")
    pg.display.set_icon(personaje)
    fuente=pg.font.SysFont("Broadway",25)
    texto=fuente.render("Lost Kingdom",True,snow)
    texto_info=pg.font.SysFont("Comic Sans MS",14)
    flag=True
    music_flag=False
    _punto_=''
    clock = pg.time.Clock()
    sonidos=cargar_sonidos()
    # (x,y,largo,ancho)
    entrada_ver = InputBox(800,170, 140, 32,1,Font)
    entrada_cambiar = InputBox(800, 270, 140, 32,2,Font)
    entrada_prof = InputBox(800, 370, 140, 32,3,Font)
    entrada_prioridad = InputBox(800, 450, 140, 32,4,Font)
    input_boxes = [entrada_ver,entrada_cambiar,entrada_prof,entrada_prioridad]
    #input_boxes = [entrada_ver,entrada_cambiar]
    j=0
    i=0
    j1=False
    mostrar_v=True
    while flag:
        
        if music_flag == False:
            pg.mixer.music.play(3)
            music_flag=True
        #pygame.fill(negro)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag=False
            for box in input_boxes:
                box.handle_event(event)
                
        for box in input_boxes:
            box.update()
        #ancho,alto     
        input_boxes[2].prioridad=input_boxes[3].prioridad
        marco_img= pg.transform.scale(marco, [300, 600])
        ventana.blit(marco_img,[750,0])
        ventana.blit(texto,[810,50])
        mostrar_texto(ventana,"Comic Sans MS",14,"Ver un punto:",800,150,snow)
        mostrar_texto(ventana,"Comic Sans MS",12, "Ejemplo:(5,B) Dar enter para enviar",800,210,snow)
        mostrar_texto(ventana,"Comic Sans MS",14,"Cambiar un punto:",800,250,snow)
        mostrar_texto(ventana,"Comic Sans MS",12, "Ejemplo:(5,B)->Paso /(Muro)",800,310,snow)
        mostrar_texto(ventana,"Comic Sans MS",12, "Dar enter para enviar",800,325,snow)
        mostrar_texto(ventana,"Comic Sans MS",12,"Prioridad: "+input_boxes[2].prioridad ,770,30,snow)
        mostrar_texto(ventana,"Comic Sans MS",14, "Algoritmo de Profunidad",800,350,snow)
        mostrar_texto(ventana,"Comic Sans MS",14, "Cambiar prioridad:",800,430,snow)
        if mostrar_v == True:
            muros_mapa=construir_mapa(mapa)
            dibujar(ventana,muros_mapa,True)
        for box in input_boxes:
            box.draw(ventana)
        if input_boxes[2].successful == True:
            if j == 0:
                _inicio_=coordenas_mapa(input_boxes[2].coordenadaI)
                _final_=coordenas_mapa(input_boxes[2].coordenadaF)             
                mostrar_laberinto_pasos(diferentes_pos(_inicio_[0],_inicio_[1]), mapa,_inicio_[1],_inicio_[0])
                filaf=mapa[_final_[0]]
                p_f=filaf[_final_[1]]
                p_f.ver=True
                sonidos[0].play()
                pg.time.delay(1500)
                j=1
                mostrar_v=False
            else:
                rutas=input_boxes[2].camino
                movimiento=rutas[i]
                xy=movimiento[1]
                mostrar_laberinto_pasos(diferentes_pos(xy[0],xy[1]), mapa,xy[1],xy[0])
                muros_mapa=construir_mapa(mapa)
                dibujar(ventana,muros_mapa,True)
                picture = pg.transform.scale(personaje, [50, 40])
                ventana.blit(picture,[xy[1]*50,xy[0]*40])
                
                i+=1
                if i == len(rutas):
                    j=0
                    input_boxes[2].successful=False
                    limpiar_mapa(mapa)
                    mostrar_texto(ventana,"SHOWCARD GOTHIC",40, "\"Has llegado\"",270,200,sand)
                    sonidos[1].play(1)
                    mostrar_v=True
                    i=0 
                    pg.display.update()
                    pg.time.delay(350)
                pg.time.delay(350)
        if input_boxes[2].error == True:
            mostrar_texto(ventana,"SHOWCARD GOTHIC",40, "\"ERROR\"",270,200,rojo)
            sonidos[2].play(1)
            pg.display.update()
            input_boxes[2].error=False
            pg.time.delay(700)
        for l in coordena:
            mostrar_texto(ventana,"Comic Sans MS",16,l[1],((l[0]*50)+25),0,azul)
            mostrar_texto(ventana,"Comic Sans MS",16,str(l[0]+1),0,((l[0]*40)+10),azul)
        input_boxes[0].draw_text(ventana,850,125,20)
        pg.time.delay(100)
        pg.display.update()
        
    pg.quit()# cerrar display
    
    



