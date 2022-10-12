import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import matplotlib as mpl
from matplotlib import cm
import math
import cycler
from scipy.stats import t

n = 4
color = mpl.cm.viridis(np.linspace(0.0, 1.0, n))
plt.rcParams['axes.prop_cycle'] = cycler.cycler(color=color)

# Old validations (first version)
def viridis(a, b, color_amount):
    color = mpl.cm.viridis(np.linspace(a, b, n))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)

# My validations

def valid_single_simulation():
    viridis(0.0, 1.0, 2)

    # Simulation results parameters
    domain = 'lambda'
    anti_domain = 'beAirTime'

    sim1_label = "5G-Coex-SimPy"
    sim1 = pd.read_csv('csvresults/VAL/LAMBDA/peak/peak_simulation_v1.csv', delimiter=',')

    x_axis_description = "Lambda"
    y_axis_description = "Channel occupancy"

    y_range = (0, 0.7)
    result_file_path = 'results/VAL/lambda/peak/peak-v1.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_std = sim1.groupby([domain]).std().loc[:, anti_domain]

    # Calculating number of probes
    sim1_n = sim1.groupby([domain]).count().loc[:, anti_domain]

    # Calculating error for each probe
    sim1_err = sim1_std / np.sqrt(sim1_n) * t.ppf(1 - alfa / 2, sim1_n - 1)

    # Results grouping
    sim1 = sim1.groupby([domain])[anti_domain].mean()

    # Results plotting
    sim1_plot = sim1.plot(marker='o', legend=True,ylim=y_range,yerr=sim1_err,capsize=4)

    sim1_plot.legend([sim1_label])
    sim1_plot.set_xlabel(x_axis_description, fontsize=14)
    sim1_plot.set_ylabel(y_axis_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file_path)

def valid_two_simulations():
    viridis(0.0, 1.0, 2)

    # Simulation results parameters
    domain = 'nss'
    anti_domain = 'Throughput'

    sim1_label = "ns-3"
    sim2_label = "5G-Coex-SimPy"

    sim1 = pd.read_csv('csvresults/VAL/80211ac/nss/ns3-nss-v1.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/VAL/80211ac/nss/sp-nss-v1.csv', delimiter=',')

    x_axis_description = "Number of Spatial Streams"
    y_axis_description = "Throughput [Mb/s]"
    linestyle="solid"

    y_range = (0,100)
    result_file_path = 'results/VAL/ac/nSS/sp-nss-v1.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_std = sim1.groupby([domain]).std().loc[:, anti_domain]
    sim2_std = sim2.groupby([domain]).std().loc[:, anti_domain]

    # Calculating number of probes
    sim1_n = sim1.groupby([domain]).count().loc[:, anti_domain]
    sim2_n = sim2.groupby([domain]).count().loc[:, anti_domain]

    # Calculating error for each probe
    sim1_err = sim1_std / np.sqrt(sim1_n) * t.ppf(1-alfa/2,sim1_n-1)
    sim2_err = sim2_std / np.sqrt(sim2_n) * t.ppf(1-alfa/2,sim2_n-1)

    # Results grouping
    sim1 = sim1.groupby([domain])[anti_domain].mean()
    sim2 = sim2.groupby([domain])[anti_domain].mean()

    # Results plotting
    sim1_plot = sim1.plot(marker='o', legend=True, capsize=4, yerr = sim1_err,ylim=y_range,linestyle=linestyle,mfc='none')
    sim2_plot = sim2.plot(ax=sim1_plot, marker='x', legend=True, capsize=4, yerr = sim2_err,linestyle=linestyle)

    # log scale
    #sim1_plot.set_xscale('log')

    sim2_plot.legend([sim1_label,sim2_label])
    sim2_plot.set_xlabel(x_axis_description, fontsize=14)
    sim2_plot.set_ylabel(y_axis_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file_path)

def valid_four_simulations():
    viridis(0.0, 1.0, 2)

    domain = 'retryLimit'
    anti_domain_1 = 'PcollNR'
    anti_domain_2 = 'PcollWiFi'

    sim1_1_label = "MATLAB: NR-U"
    sim1_2_label = "MATLAB: WiFi"
    sim2_1_label = "5G-Coex-SimPy: NR-U"
    sim2_2_label = "5G-Coex-SimPy: WiFi"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/VAL/Coex/r/matlab-coex-r-v1.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/VAL/Coex/r/coex-r-v1.csv', delimiter=',')

    OX_description = "Retry limit"
    OY_description = "Collision probability"
    result_file='results/VAL/Coex/r/coex-r-cp-v1.svg'

    lim_range = (0,1)
    linestyle = "dashed"
    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1.groupby([domain]).std().loc[:, anti_domain_1]
    sim1_2_std = sim1.groupby([domain]).std().loc[:, anti_domain_2]
    sim2_1_std = sim2.groupby([domain]).std().loc[:, anti_domain_1]
    sim2_2_std = sim2.groupby([domain]).std().loc[:, anti_domain_2]

    # Calculating number of probes
    sim1_1_n = sim1.groupby([domain]).count().loc[:, anti_domain_1]
    sim1_2_n = sim1.groupby([domain]).count().loc[:, anti_domain_2]
    sim2_1_n = sim2.groupby([domain]).count().loc[:, anti_domain_1]
    sim2_2_n = sim2.groupby([domain]).count().loc[:, anti_domain_2]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    sim2_1_err = sim2_1_std / np.sqrt(sim2_1_n) * t.ppf(1 - alfa / 2, sim2_1_n - 1)
    sim2_2_err = sim2_2_std / np.sqrt(sim2_2_n) * t.ppf(1 - alfa / 2, sim2_2_n - 1)

    # Results grouping
    sim1_1 = sim1.groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim1.groupby([domain])[anti_domain_2].mean()
    sim2_1 = sim2.groupby([domain])[anti_domain_1].mean()
    sim2_2 = sim2.groupby([domain])[anti_domain_2].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='x', legend=True,yerr=sim1_1_err,capsize=4,ylim=lim_range,linestyle=linestyle)
    ax2 = sim1_2.plot(ax=ax1, marker='x', legend=True,yerr=sim1_2_err,capsize=4,linestyle=linestyle)
    ax3 = sim2_1.plot(ax=ax2,marker='o', legend=True,yerr=sim2_1_err,capsize=4,mfc='none',linestyle=linestyle)
    ax4 = sim2_2.plot(ax=ax3, marker='o', legend=True,yerr=sim2_2_err,capsize=4,mfc='none',linestyle=linestyle)

    # log scale option
    #ax4.set_xscale('log')

    ax4.legend([sim1_1_label,sim1_2_label,sim2_1_label,sim2_2_label])
    ax4.set_xlabel(OX_description, fontsize=14)
    ax4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_four_simulations():
    viridis(0.0, 1.0, 2)

    domain = 'WiFi'
    anti_domain_1 =  'thrpt_vc'
    anti_domain_2 =  'thrpt_vd'
    anti_domain_3 =  'thrpt_be'
    anti_domain_4 =  'thrpt_bg'

    sim1_1_label = "5G-Coex-SimPy: AC_VO"
    sim1_2_label = "5G-Coex-SimPy: AC_VI"
    sim1_3_label = "5G-Coex-SimPy: AC_BE"
    sim1_4_label = "5G-Coex-SimPy: AC_BK"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/VAL/LAMBDA/lambda-edca/lambda-edca-st-v1.csv', delimiter=',')

    OX_description = "Total number of stations"
    OY_description = "Channel occupancy"
    result_file = 'results/VAL/LAMBDA/lambda-edca/lambda-st-edca-v1.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1.groupby([domain]).std().loc[:, anti_domain_1]
    sim1_2_std = sim1.groupby([domain]).std().loc[:, anti_domain_2]
    sim1_3_std = sim1.groupby([domain]).std().loc[:, anti_domain_3]
    sim1_4_std = sim1.groupby([domain]).std().loc[:, anti_domain_4]

    # Calculating number of probes
    sim1_1_n = sim1.groupby([domain]).count().loc[:, anti_domain_1]
    sim1_2_n = sim1.groupby([domain]).count().loc[:, anti_domain_2]
    sim1_3_n = sim1.groupby([domain]).count().loc[:, anti_domain_3]
    sim1_4_n = sim1.groupby([domain]).count().loc[:, anti_domain_4]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)
    sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_4_n - 1)

    # Results grouping
    sim1_1 = sim1.groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim1.groupby([domain])[anti_domain_2].mean()
    sim1_3 = sim1.groupby([domain])[anti_domain_3].mean()
    sim1_4 = sim1.groupby([domain])[anti_domain_4].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='o', legend=True , ylim=(0,50), mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4 )
    ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True , mfc='none',yerr=sim1_3_err,capsize=4)
    ax4 = sim1_4.plot(ax=ax3, marker='o', legend=True,yerr=sim1_4_err,capsize=4)

    # log scale option
    #ax4.set_xscale('log')

    ax4.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label])
    ax4.set_xlabel(OX_description, fontsize=14)
    ax4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)


if __name__ == "__main__":
    #print_four_simulations()
    #valid_single_simulation()
    #valid_four_simulations()
    valid_two_simulations()




