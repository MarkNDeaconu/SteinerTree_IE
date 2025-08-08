import numpy as np
from numpy.fft import rfft, irfft

def tree_combination_sum_fft(r1, r2, weight, bf):
    a = np.array([bf(r1, i) for i in range(weight + 1)], dtype=np.float64)
    b = np.array([bf(r2, i) for i in range(weight + 1)], dtype=np.float64)

    n = 1 << (2 * weight).bit_length()
    a = np.pad(a, (0, n - len(a)))
    b = np.pad(b, (0, n - len(b)))

    A = rfft(a)
    B = rfft(b)
    C = A * B
    c = irfft(C)

    result = round(c[weight])
    return result

#this way is far too slow
'''
import mpmath as mp

def mp_fft(x):
    """Recursive Cooley–Tukey FFT with arbitrary precision complex numbers."""
    N = len(x)
    if N <= 1:
        return x
    even = mp_fft(x[0::2])
    odd = mp_fft(x[1::2])
    T = [mp.e**(-2j * mp.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + \
           [even[k] - T[k] for k in range(N // 2)]

def mp_ifft(X):
    N = len(X)
    conj_X = [mp.conj(val) for val in X]
    inv = mp_fft(conj_X)
    return [mp.conj(val) / N for val in inv]

def tree_combination_sum_fft(r1, r2, weight, bf, prec=64):
    mp.mp.dps = prec  # set decimal precision

    # Make sure inputs are complex from the start
    a = [mp.mpc(bf(r1, i), 0) for i in range(weight + 1)]
    b = [mp.mpc(bf(r2, i), 0) for i in range(weight + 1)]

    n = 1 << (2 * weight).bit_length()
    a += [mp.mpc(0) for _ in range(n - len(a))]
    b += [mp.mpc(0) for _ in range(n - len(b))]

    A = mp_fft(a)
    B = mp_fft(b)
    C = [A[i] * B[i] for i in range(n)]
    c = mp_ifft(C)

    # Take real part before rounding
    return mp.nint(c[weight].real)
'''

def tree_combination_sum(r1, r2, weight, bf):
    #Divides the r1 simplified problem into one between two roots: r1 and it's neighbor r2
    # Uses the number of branching walks starting from r1 of specific weights less than the max, as well as the same for r2. 
    #Takes that info from the dynamic programming table and combines it in order to come up with the count of 'double rooted' branching walks

    sum = 0
    #theoretical concern: this seems wrong because it multiple counts the number of branching walks when w2 = 0
    for w1 in range(weight+1):
        w2 = weight - w1
        
        sum += bf(r1,w1) * bf(r2, w2)
    
    return(sum)