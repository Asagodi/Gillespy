import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

def ssa(input_values, params, rate_list, change_list):
    values = input_values
    ##The rate at which any event occurs is
    rate_list_vals =  [rli(input_values, params) for i,rli in enumerate(rate_list)]
    ratesum = sum(rate_list_vals)
    ## The time until the next event is
    delta_t = -np.log(np.random.uniform())/ratesum
    ##Generate a new random number and set
    P = np.random.uniform() * ratesum
    sumpl = 0
    sumpr = 0
    for i, ri in enumerate(rate_list_vals):
##        print sumpl, sumpr
        sumpr += rate_list_vals[i]
        if sumpl < P < sumpr:
####            print change_list[i,:].dot(ri)
            values = input_values + change_list[i,:]
##            print values
        sumpl += ri
    return values, delta_t

def siteration(initial_values, params, rate_list, change_list, maxtime):
    values = initial_values
    S=[initial_values[0]]
    I=[initial_values[1]]
    R=[initial_values[2]]
    time = 0
    time_list = [time]
    while time < maxtime:
        values, delta_t = ssa(values, params, rate_list, change_list)
        S.append(values[0])
        I.append(values[1])
        R.append(values[2])
        time += delta_t
        time_list.append(time)
##        if values[1] == 0:
##            return time_list, S, I, R
    return [time_list, S, I, R]
                    

rate_list = [lambda y, p: p[1]*y[0]*y[1]/p[0],
             lambda y, p: p[2]*y[1]]

##deltas = np.array()
initial_values = [999, 1, 0]
params = [1000, 0.45, 0.25]
maxtime = 0.25 * 365
change_list = np.array([(-1, 1, 0), (0, -1, 1)])
##ssa(initial_values, params, rate_list, change_list)

[tT, S, I, R] = siteration(initial_values, params, rate_list, change_list, maxtime)

pl.subplot(311)
pl.plot(tT, S, 'g')
#pl.xlabel ('Time (years)')
pl.ylabel ('Susceptible')
pl.subplot(312)
pl.plot(tT, I, 'r')
#pl.xlabel ('Time (years)')
pl.ylabel ('Infectious')
pl.subplot(313)
pl.plot(tT, R, 'k')
pl.xlabel ('Time (years)')
pl.ylabel ('Recovered')
plt.show()
