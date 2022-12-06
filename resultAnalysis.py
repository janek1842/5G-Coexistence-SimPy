import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import matplotlib as mpl
from matplotlib import cm
import math
import cycler
from scipy.stats import t
from matplotlib.ticker import MaxNLocator

n = 8
color = mpl.cm.viridis(np.linspace(0.0, 1.0, n))
plt.rcParams['axes.prop_cycle'] = cycler.cycler(color=color)

# Old validations (first version)
def viridis(a, b, color_amount):
    color = mpl.cm.viridis(np.linspace(a, b, color_amount))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)

# My validations

def valid_single_simulation():
    viridis(0.0, 2.0, 2)

    # Simulation results parameters
    domain = 'WiFi'
    anti_domain = 'Throughput'

    sim1_label = "5G-Coex-SimPy"
    sim1 = pd.read_csv('csvresults/VAL/STD/stations/sp-st-erlang-v2.csv', delimiter=',')

    x_axis_description = "Total number of stations"
    y_axis_description = "Throughput [Mb/s]"

    y_range = (0, 50)
    result_file_path = 'results/VAL/STD/stations/erlang-stations-v2.svg'

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
    sim1_plot.xaxis.set_major_locator(MaxNLocator(integer=True))
    #sim1_plot.set_xscale('log')

    sim1_plot.legend([sim1_label])
    sim1_plot.set_xlabel(x_axis_description, fontsize=14)
    sim1_plot.set_ylabel(y_axis_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file_path)

def valid_two_simulations():
    viridis(0.0, 1.0, 4)

    # Simulation results parameters
    domain = 'WiFi'
    anti_domain = 'Throughput'

    sim1_label = "5G-Coex-SimPy: RTS/CTS ON"
    sim2_label = "5G-Coex-SimPy: RTS/CTS OFF"

    sim1 = pd.read_csv('csvresults/VAL/RTS/st2/st2-v2-on.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/VAL/RTS/st2/st2-v2-off.csv', delimiter=',')

    x_axis_description = "Total number of stations"
    y_axis_description = "Throughput [Mb/s]"
    linestyle="solid"

    y_range = (0,50)
    result_file_path = 'results/VAL/RTS/st2/sp-st2-v2.svg'

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

    sim2_plot.xaxis.set_major_locator(MaxNLocator(integer=True))

    # log scale
    #sim1_plot.set_xscale('log')

    sim2_plot.legend([sim1_label,sim2_label])
    sim2_plot.set_xlabel(x_axis_description, fontsize=14)
    sim2_plot.set_ylabel(y_axis_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file_path)

def valid_four_simulations():
    viridis(0.0, 2.0, 2)

    domain = 'WiFi'
    anti_domain_1 = 'thrpt_be'
    anti_domain_2 = 'thrpt_bg'

    sim1_1_label = "ns-3: AC_BE"
    sim1_2_label = "ns-3: AC_BK"
    sim2_1_label = "5G-Coex-SimPy: AC_BE"
    sim2_2_label = "5G-Coex-SimPy: AC_BK"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/VAL/EDCA/stations/v1/ns3-beandbg-v1.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/VAL/EDCA/stations/v1/thrpt-st-beandbg-v1.csv', delimiter=',')

    OX_description = "Total number of stations"
    OY_description = "Throughput [Mb/s]"
    result_file='results/VAL/EDCA/stations/thrpt/stations-beandbg-v1.svg'

    lim_range = (0,50)
    linestyle = "solid"
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

    ax4.xaxis.set_major_locator(MaxNLocator(integer=True))
    # log scale option
    #ax4.set_xscale('log')

    ax4.legend([sim1_1_label,sim1_2_label,sim2_1_label,sim2_2_label])
    ax4.set_xlabel(OX_description, fontsize=14)
    ax4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_four_simulations():
    viridis(0.0, 1.0, 2)

    domain = 'buffer'
    anti_domain_1 =  'vcAirTime'
    anti_domain_2 =  'vdAirTime'
    anti_domain_3 =  'beAirTime'
    anti_domain_4 =  'bgAirTime'

    sim1_1_label = "5G-Coex-SimPy: AC_VO"
    sim1_2_label = "5G-Coex-SimPy: AC_VI"
    sim1_3_label = "5G-Coex-SimPy: AC_BE"
    sim1_4_label = "5G-Coex-SimPy: AC_BK"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/VAL/edca-buffer/buffer-v2.csv', delimiter=',')

    OX_description = "Buffer size [Number of frames]"
    OY_description = "Channel occupancy"
    result_file = 'results/VAL/edca-buffer/edca-buffer-v2.svg'

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
    ax1 = sim1_1.plot(marker='o', legend=True , ylim=(0,0.5), mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4 )
    ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True , mfc='none',yerr=sim1_3_err,capsize=4)
    ax4 = sim1_4.plot(ax=ax3, marker='o', legend=True,yerr=sim1_4_err,capsize=4)

    # log scale option
    ax4.set_xscale('log')

    ax4.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label])
    ax4.set_xlabel(OX_description, fontsize=14)
    ax4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_buffer_simulations():
    viridis(1.1, 0, 4)

    domain = 'lambda'
    anti_domain_1 =  'thrpt_vc'

    sim1_1_label = "5G-Coex-SimPy: K=2"
    sim1_2_label = "5G-Coex-SimPy: K=4"
    sim1_3_label = "5G-Coex-SimPy: K=6"
    sim1_4_label = "5G-Coex-SimPy: K=8"
    sim1_5_label = "5G-Coex-SimPy: K=10"
    sim1_6_label = "5G-Coex-SimPy: K=20"
    sim1_7_label = "5G-Coex-SimPy: K=1000"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/VAL/edca-buffer/buffer-v1.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Throughput [Mb/s]"
    result_file = 'results/VAL/buffer/buffer-3.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1[sim1['buffer'] == 2].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_2_std = sim1[sim1['buffer'] == 4].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_3_std = sim1[sim1['buffer'] == 6].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_4_std = sim1[sim1['buffer'] == 8].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_5_std = sim1[sim1['buffer'] == 10].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_6_std = sim1[sim1['buffer'] == 20].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_7_std = sim1[sim1['buffer'] == 1000].groupby([domain]).std().loc[:,anti_domain_1]

    # Calculating number of probes
    sim1_1_n = sim1[sim1['buffer'] == 2].groupby([domain]).count().loc[:,anti_domain_1]
    sim1_2_n = sim1[sim1['buffer'] == 4].groupby([domain]).count().loc[:,anti_domain_1]
    sim1_3_n = sim1[sim1['buffer'] == 6].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_4_n = sim1[sim1['buffer'] == 8].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_5_n = sim1[sim1['buffer'] == 10].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_6_n = sim1[sim1['buffer'] == 20].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_7_n = sim1[sim1['buffer'] == 1000].groupby([domain]).count().loc[:, anti_domain_1]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)
    sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_4_n - 1)
    sim1_5_err = sim1_5_std / np.sqrt(sim1_5_n) * t.ppf(1 - alfa / 2, sim1_5_n - 1)
    sim1_6_err = sim1_6_std / np.sqrt(sim1_6_n) * t.ppf(1 - alfa / 2, sim1_6_n - 1)
    sim1_7_err = sim1_7_std / np.sqrt(sim1_7_n) * t.ppf(1 - alfa / 2, sim1_7_n - 1)

    # Results grouping
    sim1_1 = sim1[sim1['buffer'] == 2].groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim1[sim1['buffer'] == 4].groupby([domain])[anti_domain_1].mean()
    sim1_3 = sim1[sim1['buffer'] == 6].groupby([domain])[anti_domain_1].mean()
    sim1_4 = sim1[sim1['buffer'] == 8].groupby([domain])[anti_domain_1].mean()
    sim1_5 = sim1[sim1['buffer'] == 10].groupby([domain])[anti_domain_1].mean()
    sim1_6 = sim1[sim1['buffer'] == 20].groupby([domain])[anti_domain_1].mean()
    sim1_7 = sim1[sim1['buffer'] == 1000].groupby([domain])[anti_domain_1].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='o', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4 )
    ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True , mfc='none',yerr=sim1_3_err,capsize=4)
    ax4 = sim1_4.plot(ax=ax3, marker='o', legend=True,yerr=sim1_4_err,capsize=4)
    ax5 = sim1_5.plot(ax=ax4,marker='o', legend=True, mfc='none', yerr=sim1_5_err, capsize=4)
    ax6 = sim1_6.plot(ax=ax5, marker='o', legend=True, yerr=sim1_6_err, capsize=4)
    ax7 = sim1_7.plot(ax=ax6, marker='o',ylim=(0, 15), legend=True, mfc='none', yerr=sim1_7_err, capsize=4)

    # log scale option
    #ax4.set_xscale('log')

    ax7.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label,sim1_5_label, sim1_6_label, sim1_7_label])
    ax7.set_xlabel(OX_description, fontsize=14)
    ax7.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_buffer_simulations_v2():
    viridis(0.9, 0, 3)

    domain = 'lambda'
    anti_domain_1 =  'thrpt_be'

    sim1_1_label = "5G-Coex-SimPy: K=2"
    sim1_4_label = "5G-Coex-SimPy: K=8"
    sim1_7_label = "5G-Coex-SimPy: K=1000"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/VAL/edca-buffer/buffer-v1.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Throughput [Mb/s]"
    result_file = 'results/VAL/buffer/buffer-3.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1[sim1['buffer'] == 2].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_4_std = sim1[sim1['buffer'] == 8].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_7_std = sim1[sim1['buffer'] == 1000].groupby([domain]).std().loc[:,anti_domain_1]

    # Calculating number of probes
    sim1_1_n = sim1[sim1['buffer'] == 2].groupby([domain]).count().loc[:,anti_domain_1]
    sim1_4_n = sim1[sim1['buffer'] == 8].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_7_n = sim1[sim1['buffer'] == 1000].groupby([domain]).count().loc[:, anti_domain_1]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_4_n - 1)
    sim1_7_err = sim1_7_std / np.sqrt(sim1_7_n) * t.ppf(1 - alfa / 2, sim1_7_n - 1)

    # Results grouping
    sim1_1 = sim1[sim1['buffer'] == 2].groupby([domain])[anti_domain_1].mean()
    sim1_4 = sim1[sim1['buffer'] == 8].groupby([domain])[anti_domain_1].mean()
    sim1_7 = sim1[sim1['buffer'] == 1000].groupby([domain])[anti_domain_1].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='o', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax4 = sim1_4.plot(ax=ax1, marker='o', legend=True,yerr=sim1_4_err,capsize=4)
    ax7 = sim1_7.plot(ax=ax4, marker='o',ylim=(0, 30), legend=True, mfc='none', yerr=sim1_7_err, capsize=4)

    # log scale option
    #ax4.set_xscale('log')

    ax7.legend([sim1_1_label, sim1_4_label, sim1_7_label])
    ax7.set_xlabel(OX_description, fontsize=14)
    ax7.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)


if __name__ == "__main__":
    #print_four_simulations()
    #valid_single_simulation()
    #valid_four_simulations()
    valid_two_simulations()
    #print_buffer_simulations_v2()







