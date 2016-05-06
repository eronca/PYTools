#!/usr/bin/python                                                                                                                                             \


import os
import numpy as np
from scipy import fft, arange

def run_fft(real_RTGF, imag_RTGF, eta):
    time_array = real_RTGF.transpose()[0]
    npoints = time_array.shape[0]
    delta_t = time_array[1]

    frq = np.fft.fftfreq(npoints, delta_t)
    frq = np.fft.fftshift(frq)*2.0*np.pi

    real_part = real_RTGF.transpose()[1]
    imag_part = imag_RTGF.transpose()[1]
    fftinp = 1j*(real_part - 1j*imag_part)

    for i in range(npoints):
        fftinp[i] = fftinp[i]*np.exp(-eta*time_array[i])

    Y = fft(fftinp)
    Y = np.fft.fftshift(Y)

    Y_real = Y.real
    Y_real = (Y_real*time_array[-1]/npoints)
    Y_imag = Y.imag
    Y_imag = (Y_imag*time_array[-1]/npoints)/np.pi

    # Plot the results
    with open('ldos.out', 'w') as fout:
        fout.write('#     Omega          A(Omega)\n')
        for i in range(npoints):
            fout.write('%6.3f  %8.4f\n' % (frq[i], Y_imag[i]))

    with open('real_part.txt', 'w') as fout:
        fout.write('#     Omega          A(Omega)\n')
        for i in range(npoints):
            fout.write('%6.3f  %8.4f\n' % (frq[i], Y_real[i]))



if __name__=="__main__":
    import sys, math
   
    real_RTGF = np.loadtxt("rt_real.txt") 
    imag_RTGF = np.loadtxt("rt_imag.txt")

    eta = float(sys.argv[1])
   
    run_fft(real_RTGF, imag_RTGF, eta)
