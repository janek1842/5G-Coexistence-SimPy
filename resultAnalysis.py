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
    domain = 'lambda'
    anti_domain = 'latency_be'

    sim1_label = "5G-Coex-SimPy"
    sim1 = pd.read_csv('csvresults/V6/testLevel.csv', delimiter=',')

    x_axis_description = "Lambda"
    y_axis_description = "Latency [s]"

    result_file_path = 'csvresults/V6/testLevel.svg'

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
    sim1_plot = sim1.plot(marker='o', legend=True,yerr=sim1_err,capsize=4)
    sim1_plot.xaxis.set_major_locator(MaxNLocator(integer=True))
    # log scale
    #sim1_plot.set_xscale('log')

    sim1_plot.legend([sim1_label])
    sim1_plot.set_xlabel(x_axis_description, fontsize=14)
    sim1_plot.set_ylabel(y_axis_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file_path)

def valid_two_simulations():
    viridis(0.0, 1.0, 2)

    # Simulation results parameters
    domain = 'lambda'
    anti_domain_1 = 'ChannelOccupancyNR'
    anti_domain_2 = 'ChannelOccupancyWiFi'

    sim1_label = "5G-Coex-SimPy: Wi-Fi"
    sim2_label = "5G-Coex-SimPy: NR-U"

    sim1 = pd.read_csv('csvresults/V4/latency/test5.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/V4/test300.svg', delimiter=',')

    x_axis_description = "CWmin"
    y_axis_description = "Channel occupancy"
    linestyle="solid"

    y_range = (0,1)
    result_file_path = 'results/VAL/WiFi/stations/cot/cot-stations-v10.svg'

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
    sim1_plot.set_xscale('log')

    sim2_plot.legend([sim1_label,sim2_label])
    sim2_plot.set_xlabel(x_axis_description, fontsize=14)
    sim2_plot.set_ylabel(y_axis_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file_path)

def valid_four_simulations():
    viridis(0.0, 3.0, 8)

    domain = 'lambda'
    anti_domain_1 = 'ChannelOccupancyWiFi'
    anti_domain_2 = 'ChannelOccupancyNR'

    sim1_1_label = "Black Simulation: WiFi K=3000"
    sim1_2_label = "Black Simulation: NR-U K=3000"

    sim2_1_label = "Red Simulation: WiFi K=1"
    sim2_2_label = "Red Simulation: NR-U K=3000000"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/V4/latency/test5.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/V4/latency/test6.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Channel occupancy"
    result_file='csvresults/latency600.svg'

    lim_range = (0,1)
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
    ax4 = sim2_2.plot(ax=ax3, marker='o', legend=True,yerr=sim2_2_err,capsize=4,mfc='none',xlim=[0,0.15],linestyle=linestyle)

    ax4.xaxis.set_major_locator(MaxNLocator(integer=True))
    # log scale option
    #ax4.set_xscale('log')

    ax4.legend([sim1_1_label,sim1_2_label,sim2_1_label,sim2_2_label])
    ax4.set_xlabel(OX_description, fontsize=14)
    ax4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_four_simulations():
    viridis(1.2, 0, 4)

    domain = 'lambda'
    anti_domain_1 =  'c1AirTime'
    anti_domain_2 =  'c3AirTime'
    anti_domain_3 =  'beAirTime'
    anti_domain_4 =  'vcAirTime'

    sim1_1_label = "5G-Coex-SimPy: CLASS 1"
    sim1_2_label = "5G-Coex-SimPy: CLASS 3"
    sim1_3_label = "5G-Coex-SimPy: AC_BE"
    sim1_4_label = "5G-Coex-SimPy: AC_VO"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/V6/testGAP3.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Channel occupancy"
    result_file = 'csvresults/V6/testGAP3.svg'

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
    ax1 = sim1_1.plot(marker='o', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4 )
    ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True , mfc='none',yerr=sim1_3_err,capsize=4)
    ax4 = sim1_4.plot(ax=ax3, marker='o', legend=True,yerr=sim1_4_err,capsize=4,ylim=[0,1])

    # log scale option
    #ax4.set_xscale('log')

    ax4.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label])
    ax4.set_xlabel(OX_description,fontsize=14)
    ax4.set_ylabel(OY_description,fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_eight_simulations():
    viridis(1, 0, 4)

    domain = 'lambda'

    anti_domain_1 =  'bgAirTime'
    anti_domain_2 =  'beAirTime'
    anti_domain_3 =  'vdAirTime'
    anti_domain_4 =  'vcAirTime'

    anti_domain_5 =  'c1AirTime'
    anti_domain_6 =  'c2AirTime'
    anti_domain_7 =  'c3AirTime'
    anti_domain_8 =  'c4AirTime'

    sim1_1_label = "AC_BG"
    sim1_2_label = "AC_BE"
    sim1_3_label = "5G-Coex-SimPy: Wi-Fi (K=3000)"
    sim1_4_label = "5G-Coex-SimPy: NR-U (K=3000)"

    sim1_5_label = "AC_BG"
    sim1_6_label = "AC_BE"
    sim1_7_label = "AC_VI"
    sim1_8_label = "AC_VO"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/V4/latency/test5.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Channel occupancy"
    result_file = 'csvresults/V4/test300.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    # sim1_1_std = sim1.groupby([domain]).std().loc[:, anti_domain_1]
    # sim1_2_std = sim1.groupby([domain]).std().loc[:, anti_domain_2]
    #sim1_3_std = sim1.groupby([domain]).std().loc[:, anti_domain_3]
    sim1_4_std = sim1.groupby([domain]).std().loc[:, anti_domain_4]
    # sim1_5_std = sim1.groupby([domain]).std().loc[:, anti_domain_5]
    # sim1_6_std = sim1.groupby([domain]).std().loc[:, anti_domain_6]
    #sim1_7_std = sim1.groupby([domain]).std().loc[:, anti_domain_7]
    sim1_8_std = sim1.groupby([domain]).std().loc[:, anti_domain_8]

    # Calculating number of probes
    # sim1_1_n = sim1.groupby([domain]).count().loc[:, anti_domain_1]
    # sim1_2_n = sim1.groupby([domain]).count().loc[:, anti_domain_2]
    #sim1_3_n = sim1.groupby([domain]).count().loc[:, anti_domain_3]
    sim1_4_n = sim1.groupby([domain]).count().loc[:, anti_domain_4]
    # sim1_5_n = sim1.groupby([domain]).count().loc[:, anti_domain_5]
    # sim1_6_n = sim1.groupby([domain]).count().loc[:, anti_domain_6]
    #sim1_7_n = sim1.groupby([domain]).count().loc[:, anti_domain_7]
    sim1_8_n = sim1.groupby([domain]).count().loc[:, anti_domain_8]

    # Calculating error for each probe
    # sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    # sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    #sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)
    sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_4_n - 1)
    # sim1_5_err = sim1_5_std / np.sqrt(sim1_5_n) * t.ppf(1 - alfa / 2, sim1_5_n - 1)
    # sim1_6_err = sim1_6_std / np.sqrt(sim1_6_n) * t.ppf(1 - alfa / 2, sim1_6_n - 1)
    #sim1_7_err = sim1_7_std / np.sqrt(sim1_7_n) * t.ppf(1 - alfa / 2, sim1_7_n - 1)
    sim1_8_err = sim1_8_std / np.sqrt(sim1_8_n) * t.ppf(1 - alfa / 2, sim1_8_n - 1)

    # Results grouping
    # sim1_1 = sim1.groupby([domain])[anti_domain_1].mean()
    # sim1_2 = sim1.groupby([domain])[anti_domain_2].mean()
    #sim1_3 = sim1.groupby([domain])[anti_domain_3].mean()
    sim1_4 = sim1.groupby([domain])[anti_domain_4].mean()
    # sim1_5 = sim1.groupby([domain])[anti_domain_5].mean()
    # sim1_6 = sim1.groupby([domain])[anti_domain_6].mean()
    #sim1_7 = sim1.groupby([domain])[anti_domain_7].mean()
    sim1_8 = sim1.groupby([domain])[anti_domain_8].mean()

    # Results plotting
    # ax1 = sim1_1.plot(marker='o', legend=True ,yerr=sim1_1_err,capsize=4,linestyle="dotted")
    # ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4,linestyle="dotted")
    #ax3 = sim1_3.plot(marker='o', legend=True ,yerr=sim1_3_err,capsize=4,linestyle="dotted")
    ax4 = sim1_4.plot(marker='o', legend=True,yerr=sim1_4_err,capsize=4,linestyle="solid")

    # ax5 = sim1_5.plot(marker='v', legend=True, yerr=sim1_5_err, capsize=4,linestyle="solid")
    # ax6 = sim1_6.plot(ax=ax5, marker='v', legend=True, yerr=sim1_6_err, capsize=4,linestyle="solid")
    #ax7 = sim1_7.plot(ax=ax4, marker='v', legend=True, yerr=sim1_7_err, capsize=4,linestyle="solid")
    ax8 = sim1_8.plot(ax=ax4, marker='v', legend=True, yerr=sim1_8_err,ylim=[0,1], capsize=4,linestyle="solid")

    # log scale option
    #ax4.set_xscale('log')

    ax8.legend([sim1_3_label, sim1_4_label],loc="upper left")

    ax8.set_xlabel(OX_description, fontsize=14)
    ax8.set_ylabel(OY_description, fontsize=14)

    #plt.tight_layout()
    plt.savefig(result_file)

def print_buffer_simulations():
    viridis(1.1, 0, 4)

    domain = 'buffer'
    anti_domain_1 =  'latency_wifi'

    sim1_1_label = "Number of stations = 2"
    sim1_2_label = "Number of stations = 10"
    sim1_3_label = "Number of stations = 20"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/V4/latency/test1.csv', delimiter=',')

    OX_description = "Buffer size [number of frames]"
    OY_description = "Average latency [s]"
    result_file = 'csvresults/V4/latency1.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1[sim1['WiFi'] == 2].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_2_std = sim1[sim1['WiFi'] == 10].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_3_std = sim1[sim1['WiFi'] == 20].groupby([domain]).std().loc[:,anti_domain_1]


    # Calculating number of probes
    sim1_1_n = sim1[sim1['WiFi'] == 2].groupby([domain]).count().loc[:,anti_domain_1]
    sim1_2_n = sim1[sim1['WiFi'] == 10].groupby([domain]).count().loc[:,anti_domain_1]
    sim1_3_n = sim1[sim1['WiFi'] == 20].groupby([domain]).count().loc[:, anti_domain_1]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)

    # Results grouping
    sim1_1 = sim1[sim1['WiFi'] == 2].groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim1[sim1['WiFi'] == 10].groupby([domain])[anti_domain_1].mean()
    sim1_3 = sim1[sim1['WiFi'] == 20].groupby([domain])[anti_domain_1].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='o', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4 )
    ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True , mfc='none',yerr=sim1_3_err,capsize=4)

    # log scale option
    #ax4.set_xscale('log')

    ax3.legend([sim1_1_label, sim1_2_label, sim1_3_label,sim1_4_label, sim1_5_label, sim1_6_label,sim1_7_label, sim1_8_label])
    ax3.set_xlabel(OX_description, fontsize=14)
    ax3.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_buffer_simulations_v2():
    viridis(1.1, 0, 6)

    k1=1
    k2=10
    k3=20
    k4=30

    domain = 'lambda'
    anti_domain_1 =  'latency_wifi'
    anti_domain_2 =  'latency_wifi'

    sim1_1_label = "K=1"
    sim1_2_label = "K=10"
    sim1_3_label = "K=20"
    sim1_4_label = "K=30"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/V4/latency/test3.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Average latency [s]"
    result_file = 'csvresults/V4/latency6.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1[sim1['buffer'] == k1].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_2_std = sim1[sim1['buffer'] == k2].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_3_std = sim1[sim1['buffer'] == k3].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_4_std = sim1[sim1['buffer'] == k4].groupby([domain]).std().loc[:, anti_domain_1]

    # Calculating number of probes
    sim1_1_n = sim1[sim1['buffer'] == k1].groupby([domain]).count().loc[:,anti_domain_1]
    sim1_2_n = sim1[sim1['buffer'] == k2].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_3_n = sim1[sim1['buffer'] == k3].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_4_n = sim1[sim1['buffer'] == k4].groupby([domain]).count().loc[:, anti_domain_1]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)
    sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)

    # Results grouping
    sim1_1 = sim1[sim1['buffer'] == k1].groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim1[sim1['buffer'] == k2].groupby([domain])[anti_domain_1].mean()
    sim1_3 = sim1[sim1['buffer'] == k3].groupby([domain])[anti_domain_1].mean()
    sim1_4 = sim1[sim1['buffer'] == k4].groupby([domain])[anti_domain_1].mean()

    # Results plotting
    ax1_1 = sim1_1.plot(marker='x', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax1_2 = sim1_2.plot(ax=ax1_1, marker='o', legend=True,yerr=sim1_2_err,capsize=4)
    ax1_3 = sim1_3.plot(ax=ax1_2, marker='v', legend=True, yerr=sim1_3_err, capsize=4)
    ax1_4 = sim1_4.plot(ax=ax1_3, marker='*', legend=True, yerr=sim1_4_err, capsize=4)

    # log scale option
    #ax4.set_xscale('log')

    ax1_4.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label])
    ax1_4.set_xlabel(OX_description, fontsize=14)
    ax1_4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

def print_nr_simulations():
    viridis(1, 0, 4)

    domain = 'lambda'

    anti_domain_1 =  'latency_c4'
    anti_domain_2 =  'latency_c3'
    anti_domain_3 =  'latency_c2'
    anti_domain_4 =  'latency_c1'

    sim1_1_label = "Class 4"
    sim1_2_label = "Class 3"
    sim1_3_label = "Class 2"
    sim1_4_label = "Class 1"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/V4/latency/test4.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Average latency [s]"
    result_file = 'csvresults/V4/test300.svg'

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
    ax1 = sim1_1.plot(marker='o', legend=True ,yerr=sim1_1_err,capsize=4,linestyle="dotted")
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4,linestyle="dotted")
    ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True ,yerr=sim1_3_err,capsize=4,linestyle="dotted")
    ax4 = sim1_4.plot(ax=ax3, marker='o', legend=True,yerr=sim1_4_err,capsize=4,linestyle="dotted")

    ax4.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label],loc="upper left")

    ax8.set_xlabel(OX_description, fontsize=14)
    ax8.set_ylabel(OY_description, fontsize=14)

    #plt.tight_layout()
    plt.savefig(result_file)


if __name__ == "__main__":
    #print_four_simulations()
    #print_eight_simulations()
    #valid_two_simulations()
    valid_single_simulation()
    #valid_four_simulations()
    #valid_two_simulations()
    #print_buffer_simulations_v2()







