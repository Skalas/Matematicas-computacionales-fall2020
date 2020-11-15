# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import mpl_toolkits.mplot3d.axes3d as a3d

from numpy import sin, cos

from utils import normalizeRads, normalizeAngle
from scipy.integrate import odeint 

class Pendulo:
    """
    Péndulo
    -----------------------
    
    El estado inicial está dado por [theta, omega] ambos en radianes.
    Theta y omega son la posición angular y la velocidad angular respectivamente.
    """
    def __init__(self, 
                 estado_inicial = [-np.pi/6, 0.],
                 masa = 1.0, # masa en kg
                 longitud = 1.0, # longitud en m
                 gravedad = 9.8, # aceleración de la gravedad, en m/s^2
                 origen=(0,0)):
                 
        self.estado_inicial = np.asarray(estado_inicial, dtype="float")
        self.estado_inicial = normalizeRads(self.estado_inicial, decimals=8) # normalizamos para estar entre [-pi, pi)
        
        self.params = (longitud, masa, gravedad)
        self.origen = origen
        self.time_elapsed = 0
        
        self.estado = self.estado_inicial
        
        self.trayectoria = self.estado
        
    
    def x(self):
    
        (longitud, masa, gravedad) = self.params
        
        return longitud*sin(self.theta())
        
    
    
    def y(self):
    
        (longitud, masa, gravedad) = self.params
        
        return -longitud*cos(self.theta())
        
    
    def theta(self):
        return self.trayectoria[:,0]
    
    def omega(self):
        return self.trayectoria[:,1]
    
   
    def dinamica(self, state, t):
        """ Ecuaciones de movimiento """
    
        (longitud, masa, gravedad) = self.params
        
        dydx = np.zeros_like(state)
    
        dydx[0] = state[1]
        dydx[1] = -(gravedad/longitud)*sin(state[0])
        
        return dydx
        
        
    def posicion(self):
        """ Calcula la posición x,y actual del péndulo. """
        (longitud, masa, gravedad) = self.params
        
        x = [self.origen[0], self.origen[0] + longitud*sin(self.estado[0])]
        y = [self.origen[1], self.origen[1] - longitud*cos(self.estado[0])]
        
        return (x,y)
        
    def energia(self):
        """ Calcula la energía mecánica """
        (longitud, masa, gravedad) = self.params
    
        U = - masa * gravedad * longitud * cos(self.estado[0])
        
        K = 0.5 * masa * longitud**2 * self.estado[1]**2
        
        return U + K
    
    
    def step(self, dt):
        """ Ejecuta un paso de tiempo, dt, y actualiza el estado. """
        self.estado = odeint(self.dinamica, self.estado, [0,dt])[1]

        self.time_elapsed += dt
       
    
    
    def integrate(self, num_steps=3000, t_i=0, t_f=30):
        """ Resuelve la dinámica en el delta de tiempo especificado """
        self.tau = np.linspace(t_i, t_f, num=num_steps)
        
        self.trayectoria = odeint(self.dinamica, self.estado_inicial, self.tau)
        
      
    def plot(self):
        """ Basado en http://debtechandstuff.blogspot.mx/2009/10/creating-video-of-3d-graph-plotting.html """
    
        fig=plt.figure(figsize=(12,6))
        fig.suptitle("Pendulo Simple", fontsize=14, fontweight='bold')


        ax = a3d.Axes3D(fig,rect=[0,0,0.6,1])
        ax.set_autoscale_on(False)
        ax.set_xlim3d((0,30))
        ax.set_ylim3d((-1,1))
        ax.set_zlim3d((-1,1))
        ax.set_xlabel(r'$t$')
        ax.set_ylabel(r'$x$')
        ax.set_zlabel(r'$y$')
        ax.plot3D(self.tau, self.x(), self.y()) 
        
        fig.subplots_adjust(left=0.66,bottom=0.05,top=0.95)

        bx = fig.add_subplot(211)
        bx.set_autoscale_on(True)
        bx.set_ylabel(r'$\theta$')
        bx.set_title('t')
        bx.plot(self.tau,self.theta())

        cx = fig.add_subplot(212)
        cx.set_autoscale_on(True)
        cx.set_ylabel(r'$\omega$')
        cx.plot(self.tau,self.omega())

        plt.show()
     
    def phase_space(self):
        plt.figure(1, figsize=(8,6))
        plt.plot(self.theta(), self.omega())
        
        plt.show()

    def xy_snapshot(self):
        plt.figure(1, figsize=(8,6))
        plt.plot(self.x(), self.y())
        
        plt.show()
    
    
    def animar(self, dt):
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                             xlim=(-2, 2), ylim=(-2, 2))
        ax.grid()

        line, = ax.plot([], [], 'o-', lw=2)
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        energy_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

        def init():
            """initialize animation"""
            line.set_data([], [])
            time_text.set_text('')
            energy_text.set_text('')
            return line, time_text, energy_text

        def animate(i):
            """perform animation step"""
            self.step(dt)
            
            line.set_data(*self.posicion())
            time_text.set_text('time = %.1f' % self.time_elapsed)
            energy_text.set_text('energy = %.3f J' % self.energia())
            return line, time_text, energy_text

        from time import time
        t0 = time()
        animate(0)
        t1 = time()
        interval = 1000 * dt - (t1 - t0)

        ani = animation.FuncAnimation(fig, animate, frames=300,
                                      interval=interval, blit=True, init_func=init)

        return ani