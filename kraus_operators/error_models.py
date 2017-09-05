"""
Error models used to simulate the different types of decoherence effects.

author: Eduardo Villasenor
created-on: 05/06/17
"""

import qutip as qt
import numpy as np
import operations as ops

# sigmas = [qt.qeye(2), qt.sigmax(), qt.sigmay(), qt.sigmaz()]

# TODO ask david if the order of the application noise gate is important


def get_sigmas(N=1, pos=0):
    sigmas = [qt.qeye([2]*N), qt.rx(np.pi, N, pos), qt.ry(np.pi, N, pos),
              qt.rz(np.pi, N, pos)]
    return sigmas


def single_qubit_gate_noise(rho, p, N=1, pos=0):
    res = rho*(1 - p)
    sigmas = get_sigmas(N, pos)
    for noise in sigmas[1:]:
        res += p/3.*(noise * rho * noise.dag())
    return res

def single_qubit_gate(rho, gate, p, N=1, pos=0):
    new_rho = gate * rho * gate.dag()
    new_rho = single_qubit_gate_noise(new_rho, p, N, pos)
    return new_rho


def two_qubit_gate_noise(rho, p, N=2, pos1=0, pos2=1):
    res = rho*(1 - p)
    sigmas_pos1 = get_sigmas(N, pos1)
    sigmas_pos2 = get_sigmas(N, pos2)

    # Compute all the possible tensor products (i x j)
    for i in sigmas_pos1:
        for j in sigmas_pos2[1:]:
            noise = i * j
            res += p/15. * (noise * rho * noise.dag())

    # Do the missing last part (i x sig0)
    j = sigmas_pos2[0]
    for i in sigmas_pos1[1:]:
        noise = i * j
        res += p/15. * (noise * rho * noise.dag())
    return res

def two_qubit_gate(rho, gate, p, N=2, pos1=0, pos2=1):
    new_rho = gate * rho * gate.dag()
    new_rho = two_qubit_gate_noise(new_rho, p, N, pos1, pos2)
    return new_rho


# def measurement_Zbasis(rho, p, N=1, pos=0):
    # NOTE: OLD funcition dont use
#     measurement, state = ops.measure_single_Zbasis(rho, N, pos, False)
#
#     if measurement == 1:
#         noisy_measurement = ops.collapse_single_Zbasis(rho, N, 1, pos, False)
#     else:
#         noisy_measurement = ops.collapse_single_Zbasis(rho, N, 0, pos, False)
#
#     noisy_measurement = (1-p)*measurement + p*noisy_measurement
#     # Flip measurement to include error
#     r = np.random.rand()
#     if r < p:
#         measurement *= -1
#
#     return measurement, noisy_measurement


def measure_single_Zbasis(rho, p, N=1, pos=0):
    X = qt.rx(np.pi, N, pos)
    rho = (1 - p)*rho + p*(X * rho * X.dag())
    measurement, collapsed_rho = ops.random_measure_single_Zbasis(rho, N, pos, True)
    return measurement, collapsed_rho

def measure_single_Zbasis_forced(rho, p, project, N=1, pos=0):
    X = qt.rx(np.pi, N, pos)
    rho = (1 - p)*rho + p*(X * rho * X.dag())
    p, collapsed_rho = ops.forced_measure_single_Zbasis(rho, N, pos, True)
    return p, collapsed_rho


def measure_single_Xbasis(rho, p, N=1, pos=0):
    Z = qt.rx(np.pi, N, pos)
    # H = qt.snot(N, pos)
    # rho = H * rho * H.dag()
    rho = (1 - p)*rho + p*(Z * rho * Z.dag())
    measurement, collapsed_rho = ops.random_measure_single_Xbasis(rho, N, pos, True)
    return measurement, collapsed_rho

def measure_single_Xbasis_forced(rho, p, project, N=1, pos=0):
    Z = qt.rx(np.pi, N, pos)
    # H = qt.snot(N, pos)
    # rho = H * rho * H.dag()
    rho = (1 - p)*rho + p*(Z * rho * Z.dag())
    p, collapsed_rho = ops.forced_measure_single_Xbasis(rho, N, pos, project, True)
    return p, collapsed_rho


def bell_pair(p):
    a = qt.bell_state('00') * qt.bell_state('00').dag()
    b = qt.bell_state('01') * qt.bell_state('01').dag() \
        + qt.bell_state('10') * qt.bell_state('10').dag() \
        + qt.bell_state('11') * qt.bell_state('11').dag()
    W = (1-p)*a + p/3.*b
    # H = qt.snot(2, 1)
    # return H*W*H.dag()
    return W