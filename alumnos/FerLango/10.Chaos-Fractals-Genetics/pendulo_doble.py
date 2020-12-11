# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import mpl_toolkits.mplot3d.axes3d as a3d

from numpy import sin, cos

from utils import normalizeRads, normalizeAngle
from scipy.integrate import odeint 

class PenduloDoble:
    """
    PenduloDoble
    ------------------------------
    
    Basado en el código de https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

    El estado inicial está dado por [theta1, omega1, theta2, omega2] en radianes,
    theta1 y omega1 son la posición y la velocidad angular de la primera masa y 
    theta2 y omega2 son la posición y la velocidad angular de la segunda masa.
    """

    def __init__(self,
                 estado_inicial =  [-np.pi, -0.0, -np.pi/2, 0.0],
                 L1=1.0,  # longitud del primer brazo en m
                 L2=1.0,  # longitud del primer brazo en m
                 M1=1.0,  # masa del primer péndulo en kg
                 M2=1.0,  # masa del segundo péndulo en kg
                 G=9.8,  # aceleración de la gravedad en m/s^2
                 origen=(0, 0)): 
        self.estado_inicial = np.asarray(estado_inicial, dtype="float")
        self.estado_inicial = normalizeRads(self.estado_inicial, decimals=8) # normalizamos para estar entre [-pi, pi)
        
        
        self.params = (L1, L2, M1, M2, G)
        self.origen = origen
        self.time_elapsed = 0

        self.estado = self.estado_inicial
        
        self.trayectoria = self.estado
    
    
    def x1(self):
        (L1, L2, M1, M2, G) = self.params

        return L1 * sin(self.theta()[:,0])
            
    def x2(self):
        (L1, L2, M1, M2, G) = self.params

        return L1 * sin(self.theta()[:,0]) + L2 * sin(self.theta()[:,1])
    
    def y1(self):
        (L1, L2, M1, M2, G) = self.params

        return -L1 * cos(self.theta()[:,0])
    
    def y2(self):
        (L1, L2, M1, M2, G) = self.params

        return -L1 * cos(self.theta()[:,0]) -L2 * cos(self.theta()[:,1])
    
    
    def theta(self):
        return self.trayectoria[:, [0,2]] 
    
    def omega(self):
        return self.trayectoria[:, [1,3]]
    
    def dinamica(self, state, t):
        """compute the derivative of the given state"""
        (M1, M2, L1, L2, G) = self.params

        dydx = np.zeros_like(state)
        dydx[0] = state[1]
        dydx[2] = state[3]

        cos_delta = cos(state[2] - state[0])
        sin_delta = sin(state[2] - state[0])

        den1 = (M1 + M2) * L1 - M2 * L1 * cos_delta * cos_delta
        dydx[1] = (M2 * L1 * state[1] * state[1] * sin_delta * cos_delta
                   + M2 * G * sin(state[2]) * cos_delta
                   + M2 * L2 * state[3] * state[3] * sin_delta
                   - (M1 + M2) * G * sin(state[0])) / den1

        den2 = (L2 / L1) * den1
        dydx[3] = (-M2 * L2 * state[3] * state[3] * sin_delta * cos_delta
                   + (M1 + M2) * G * sin(state[0]) * cos_delta
                   - (M1 + M2) * L1 * state[1] * state[1] * sin_delta
                   - (M1 + M2) * G * sin(state[2])) / den2
        
        return dydx    
        
    def path(self):
        """ Devuelve el path x,y actual de los brazos del péndulo. """
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([L1 * sin(self.trayectoria[:,0]),
                       L2 * sin(self.trayectoria[:,2])], axis=0)
        y = np.cumsum([-L1 * cos(self.trayectoria[:,0]),
                       -L2 * cos(self.trayectoria[:,2])], axis=0)
        return (x, y)

    
    def posicion(self):
        """ Calcula la posición x,y actual de los brazos del péndulo. """
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([self.origen[0],
                       L1 * sin(self.estado[0]),
                       L2 * sin(self.estado[2])])
        y = np.cumsum([self.origen[1],
                       -L1 * cos(self.estado[0]),
                       -L2 * cos(self.estado[2])])
        return (x, y)

    def energia(self):
        """ Calcula la energía mecánica """
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([L1 * sin(self.estado[0]),
                       L2 * sin(self.estado[2])])
        y = np.cumsum([-L1 * cos(self.estado[0]),
                       -L2 * cos(self.estado[2])])
        vx = np.cumsum([L1 * self.estado[1] * cos(self.estado[0]),
                        L2 * self.estado[3] * cos(self.estado[2])])
        vy = np.cumsum([L1 * self.estado[1] * sin(self.estado[0]),
                        L2 * self.estado[3] * sin(self.estado[2])])

        U = G * (M1 * y[0] + M2 * y[1])
        K = 0.5 * (M1 * np.dot(vx, vx) + M2 * np.dot(vy, vy))

        return U + K

    def step(self, dt):
        """ Ejecuta un paso de tiempo, dt, y actualiza el estado. """
        self.estado = odeint(self.dinamica, self.estado, [0, dt])[1]
        
        self.time_elapsed += dt
        
     
    def integrate(self, num_steps=3000, t_i=0, t_f=30):
        """ Resuelve la dinámica en el delta de tiempo especificado """
        self.tau = np.linspace(t_i, t_f, num=num_steps)
        
        self.trayectoria = odeint(self.dinamica, self.estado_inicial, self.tau)
        
    def plot(self):
        """ Basado en http://debtechandstuff.blogspot.mx/2009/10/creating-video-of-3d-graph-plotting.html """
    
        fig=plt.figure(figsize=(12,6))
        fig.suptitle("Pendulo Doble", fontsize=14, fontweight='bold')


        ax = a3d.Axes3D(fig,rect=[0,0,0.6,1])
        ax.set_autoscale_on(True)
        ax.set_xlabel(r'$t$')
        ax.set_ylabel(r'$x$')
        ax.set_zlabel(r'$y$')
        ax.plot3D(self.tau, self.x1(), self.y1())
        ax.plot3D(self.tau, self.x2(), self.y2()) 
        
        fig.subplots_adjust(left=0.66,bottom=0.05,top=0.95)

        bx = fig.add_subplot(211)
        bx.set_autoscale_on(True)
        bx.set_ylabel(r'$\theta_1, \theta_2$')
        bx.set_title('t')
        bx.plot(self.tau,self.theta())

        cx = fig.add_subplot(212)
        cx.set_autoscale_on(True)
        cx.set_ylabel(r'$\omega_1, \omega_2$')
        cx.plot(self.tau,self.omega())

        plt.show()
        
    def xy_snapshot(self):
        plt.figure(1, figsize=(8,6))
        plt.plot(self.x1(), self.y1())
        plt.plot(self.x2(), self.y2())
        
        plt.show()

    def phase_space(self):
        plt.figure(1, figsize=(8,6))
        plt.plot(self.theta(), self.omega(), alpha=0.6)
        
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
