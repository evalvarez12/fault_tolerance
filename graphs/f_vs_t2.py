import matplotlib.pyplot as plt
import numpy as np


def lambda_env(t, a0, a1):
    a = (a0 + a1)*t
    lamb = (1 + np.exp(-a * t))/2.
    return 1 - lamb

# OLD data
# rajas_F = [.4967, .7528, .5124, .4595, .4254, .4626, .6128, .5464, .4618,
#            .4233, .5101, .7734, .6968, .5939, .5596]
# rajas_T = [10.2622, .3397, 1.7476, 7.5603, 23.778, 18.1866, .0679, .9036, 1.8553,
#            6.6362, 9.6927, .1021, .4456, 1.5366, 4.8700]

# best_F = [.9630, .9264, .9467, .9407, .8844, .8807, .6294, .7305, .7002, .7017,
#           .9430, .8052, .9322, .9030, .9252]
# best_T = [.3236, .0788, .3428, .4122, 1.4147, .7796, .0214, .2294, .8697, 2.0219,
#           0.3274, .0298, 0.1339, .3055, .5709]
# plt.plot(rajas_T, rajas_F, 'ro', label="Experimental paramters")
# plt.plot(best_T, best_F, 'bo', label="Improved parameters")

# NEW data
epl_mine_4_f = np.load("../decomposition/Fidelity_Rajas_var=a0_epl.npy")
epl_mine_4_t = np.load("../decomposition/Times_Rajas_var=a0_epl.npy")

bk_mine_4_f = np.load("../decomposition/Fidelity_Rajas_var=a0_bk.npy")
bk_mine_4_t = np.load("../decomposition/Times_Rajas_var=a0_bk.npy")

simple_mine_4_f = np.load("../decomposition/Fidelity_Rajas_var=a0_simple.npy")
simple_mine_4_t = np.load("../decomposition/Times_Rajas_var=a0_simple.npy")


epl_mine_3_f = np.load("../decomposition/Fidelity_Rajas_var=a0_epl_ghz3.npy")
epl_mine_3_t = np.load("../decomposition/Times_Rajas_var=a0_epl_ghz3.npy")

bk_mine_3_f = np.load("../decomposition/Fidelity_Rajas_var=a0_bk_ghz3.npy")
bk_mine_3_t = np.load("../decomposition/Times_Rajas_var=a0_bk_ghz3.npy")

simple_mine_3_f = np.load("../decomposition/Fidelity_Rajas_var=a0_simple_ghz3.npy")
simple_mine_3_t = np.load("../decomposition/Times_Rajas_var=a0_simple_ghz3.npy")

plt.plot(epl_mine_4_t[:, 0], epl_mine_4_f[:, 0], 'bs-', label="EPL")
plt.plot(bk_mine_3_t[:, 0], bk_mine_4_f[:, 0], 'rs-', label="BK")
plt.plot(simple_mine_4_t[:, 0], simple_mine_4_f[:, 0], 'gs-', label="Purification")
plt.plot(epl_mine_3_t[:, 0], epl_mine_3_f[:, 0], 'b^-')
plt.plot(bk_mine_4_t[:, 0], bk_mine_3_f[:, 0], 'r^-')
plt.plot(simple_mine_3_t[:, 0], simple_mine_3_f[:, 0], 'g^-')



# Horizontals and verticals
ver = np.linspace(0.5, 1)
hor = np.linspace(0, 2)
ones = np.ones(50)
# plt.plot(0.031* ones, ver, 'y--')
# plt.plot(0.8* ones, ver, 'r--')
# plt.plot(hor, 0.95* ones, 'g--')



#
# plt.ylim([0.7, 1])
# plt.xlim([0., 1.4])
plt.ylabel(r"Fidelity", fontsize=13)
plt.xlabel(r"Time", fontsize=13)
plt.legend(fontsize=13)
plt.show()
