"""
Simple simulation to test the surface code simulation is working
without looking at plots.

Run this code using mpi4py:
mpiexec python result_one_point_model.py topology=toric distance=10 iterations=50 cycles=10 protocol=GHZ a0=0 a1=0 eta=0 time=0

created-on: 09/12/17
@author: eduardo
"""
import sys
import numpy as np
from os.path import dirname, realpath
from mpi4py import MPI
import surface_code
import layers
import matching


def lambda_env(t, a0, a1):
    a = (a0 + a1)*t
    lamb = (1 + np.exp(-a * t))/2.
    return 1 - lamb

def get_file_name(params):
    protocol = "protocol=" + params["protocol"]
    topology = "topology=" + params["topology"]
    distance = "distance=" + params["distance"]
    iterations = "iterations=" + params["iterations"]
    cycles = "cycles=" + params["cycles"]
    eta = "eta=" + params["eta"]
    a0 = "a0=" + params["a0"]
    a1 = "a1=" + params["a1"]
    time = "time=" + params["time"]

    param_names = [protocol, topology, distance, iterations, cycles,
                   eta, a0, a1, time]
    file_name = "_".join(param_names)
    return file_name

# Start the comm for mpi4py
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Get the arguments
pythonfile = sys.argv[0]
args = dict(arg.split('=') for arg in sys.argv[1:])

# Set parameters
distance = int(args["distance"])
topology = args["topology"]
iterations = int(args["iterations"])
a0 = float(args["a0"])
a1 = float(args["a1"])
cycles = int(args["cycles"])
eta = float(args["eta"])
protocol = args["protocol"]
t = float(args["time"])

# Improved parameters
# Threshold over a0
ps = 0.003
pm = 0.003
pg = 0.003
a0 = 3.0
a1 = 1/30.
eta = 1/100.
theta = .63

protocol = "thres_a0"
t = 0.113044

# Initialize fail rate
fail_rate = 0

# Initialize objects
sc = surface_code.SurfaceCode(distance, topology)
lc = layers.Layers(sc)
sc.init_error_obj(topology, ps, pm, pg, eta, a0, a1, theta, protocol)

# Choose a measurement protocol
sc.select_measurement_protocol(t, a1, "single")


# Perform measurements
for i in range(iterations):

    # Noisy measurements
    for t in range(cycles):
        sc.noisy_measurement_cycle()
        lc.add()
    sc.measure_all_stabilizers()
    lc.add()

    # Decode and apply corrections
    lc.decode()

    # Measure logical qubit
    logical = sc.measure_logical()

    if -1 in logical[0] or -1 in logical[1]:
        fail_rate += 1

    lc.reset()
    sc.reset()

fail_rate = fail_rate/float(iterations)

# Initializing variables. mpi4py requires that we pass numpy objects.
f_rate = np.zeros(1)
total = np.zeros(1)

f_rate[0] = fail_rate

# Communication: root node receives results with a collective "reduce"
comm.Reduce(f_rate, total, op=MPI.SUM, root=0)

# Root process saves the results
if comm.rank == 0:
        total = total/float(size)
        total = total/float(cycles)
        # print("size: ", size)
        # print("id: ", rank)

        args_str = get_file_name(args)
        script_path = dirname(realpath(__file__))
        file_name = (script_path + "/results/" + args_str)
        print size, "rate :", round(total[0], 7)
        print "rate :", round(total[0], 7)*cycles
        # np.save(file_name, total)
