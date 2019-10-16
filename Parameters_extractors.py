#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:56:51 2019

@author: kishor
"""

import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
pi = np.pi



gamma = 1
ep_c = 1e-5
ep_s = 1e-5
ep_est = 1e-5
ep_ea = (1/4.0)*1e-5
ep_prime = (1/2.0)*1e-5
ep_ex = (1/4.0)*1e-5
n = 1179648
ep_sa_0 = 0
ep_1 = ep_ex/(2*n)
L_max = 0
delta_est = np.sqrt((-1/2*n)*np.log(ep_est))
w_exp = 0.5+(2.3310276)/8
# delta_est = 1e-5
delta_est = 1e-2
ep_est = np.exp(-2*n*delta_est*delta_est)

def h(p):
    if p == 1 or p == 0:
        return 0
    else:
        val = -1*p*np.log2(p) - (1-p)*np.log2(1-p)
        return val    
    
def g(p):
    global gamma
    par = p/gamma
#     print(par)
    cut = (2+np.sqrt(2))/4
    if par <= cut:
        temp = 0.5 + 0.5*np.sqrt(16*par*(par-1)+ 3)
#         print(temp)
#         print(16*par*(par-1)+ 3)
        return 1-h(temp)
    else:
        return 1  
    

def diff(p):
    global gamma
    par = p/gamma
    cut = (2+np.sqrt(2))/4
    if par >= cut:
        return 0
    else:
        ga = gamma
        val = (-0.5 * (8 * p / ga**2 + 8 * (p / ga - 1) / ga) *
         (-0.5 * np.sqrt(16 * p * (p / ga - 1) / ga + 3) - 0.5) /
         (np.sqrt(16 * p * (p / ga - 1) / ga + 3) *
          (0.5 * np.sqrt(16 * p * (p / ga - 1) / ga + 3) + 0.5) * np.log(2)) -
         0.5 * (8 * p / ga**2 + 8 * (p / ga - 1) / ga) *
         np.log(-0.5 * np.sqrt(16 * p * (p / ga - 1) / ga + 3) + 0.5) /
         (np.sqrt(16 * p * (p / ga - 1) / ga + 3) * np.log(2)) +
         0.5 * (8 * p / ga**2 + 8 * (p / ga - 1) / ga) *
         np.log(0.5 * np.sqrt(16 * p * (p / ga - 1) / ga + 3) + 0.5) /
         (np.sqrt(16 * p * (p / ga - 1) / ga + 3) * np.log(2)) -
         0.5 * (8 * p / ga**2 + 8 * (p / ga - 1) / ga) /
         (np.sqrt(16 * p * (p / ga - 1) / ga + 3) * np.log(2)))
        return val

def f_min(p,p_t):
    global gamma
    par = p/p_t
    if par <= 1:
        return g(p)
    else:
        val = diff(p_t)*p +  g(p_t) - diff(p_t)*p_t
        return val

def eta(p,p_t):
    global ep_prime, ep_ea, n, gamma
    temp1 = f_min(p,p_t)
    temp2 = (1/np.sqrt(n))*2*(np.log(13)+ diff(p_t))*np.sqrt(1-2*np.log(ep_prime*ep_ea))
    temp = temp1 - temp2
    return temp

def eta_opt(p_t):
    global ep_prime, ep_ea, n, gamma, delta_est, w_exp
    prob = w_exp*gamma - delta_est
#     print(prob)
    temp = eta(prob,p_t)
    return 1*temp

x_list = np.linspace(gamma*0.75, gamma*((2+np.sqrt(2))/4), 100)
eta_list = []
for i in range(1,100):
#     print(x_list[i])
    temp = x_list[i]
    eta_list.append(eta_opt(temp))
    
output = max(eta_list)

m = n*output- 6 - 4*np.log(1.0/ep_1)

rate = m/(2*n)
print("2*n = ", 2*n)
print("m = ", m)
print("rate =", rate)