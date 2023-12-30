# libraries
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib as mpl
from matplotlib import cm
import math
import cycler
from scipy.stats import t
from matplotlib.ticker import MaxNLocator

# color map
n = 8
color = mpl.cm.viridis(np.linspace(0.0, 1.0, n))
plt.rcParams['axes.prop_cycle'] = cycler.cycler(color=color)
def viridis(a, b, color_amount):
    color = mpl.cm.viridis(np.linspace(a, b, color_amount))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)

# Results plot generation - standard simulations
def print_four_simulations(domain,m1,m2,m3,m4,label,file,file_in,lim,log_scale=False):
    viridis(1, 0, 4)

    anti_domain_1 =  m1
    anti_domain_2 =  m2
    # anti_domain_3 =  m3
    # anti_domain_4 =  m4

    sim1_1_label = "Wi-Fi"
    sim1_2_label = "NR-U"
    # sim1_3_label = "Wi-Fi AC_BE"
    # sim1_4_label = "NR-U Class 3"

    # Simulation results parameters
    sim1 = pd.read_csv(file_in, delimiter=',')
    # 'Synchronization slot duration [\u03bcs]'
    OX_description = 'Number of skipped TX opportunities'
    OY_description = label
    result_file = file

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1.groupby([domain]).std().loc[:, anti_domain_1]
    sim1_2_std = sim1.groupby([domain]).std().loc[:, anti_domain_2]
    # sim1_3_std = sim1.groupby([domain]).std().loc[:, anti_domain_3]
    # sim1_4_std = sim1.groupby([domain]).std().loc[:, anti_domain_4]

    # Calculating number of probes
    sim1_1_n = sim1.groupby([domain]).count().loc[:, anti_domain_1]
    sim1_2_n = sim1.groupby([domain]).count().loc[:, anti_domain_2]
    # sim1_3_n = sim1.groupby([domain]).count().loc[:, anti_domain_3]
    # sim1_4_n = sim1.groupby([domain]).count().loc[:, anti_domain_4]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    # sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)
    # sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_4_n - 1)

    # Results grouping
    sim1_1 = sim1.groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim1.groupby([domain])[anti_domain_2].mean()
    # sim1_3 = sim1.groupby([domain])[anti_domain_3].mean()
    # sim1_4 = sim1.groupby([domain])[anti_domain_4].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='o', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4,ylim=lim)
    # ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True , mfc='none',yerr=sim1_3_err,capsize=4)
    # ax4 = sim1_4.plot(ax=ax3, marker='o', legend=True,yerr=sim1_4_err,capsize=4,ylim=lim)
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

    # log scale option
    if log_scale:
        ax2.set_xscale('log')

    ax2.legend([sim1_1_label, sim1_2_label])
    ax2.set_xlabel(OX_description,fontsize=14)
    ax2.set_ylabel(OY_description,fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

# Results plot generation - buffer simulation v1
def print_buffer_simulations():
    viridis(1.1, 0, 4)

    domain = 'lambda'
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
    # ax4.set_xscale('log')

    ax3.legend([sim1_1_label, sim1_2_label, sim1_3_label,sim1_4_label, sim1_5_label, sim1_6_label,sim1_7_label, sim1_8_label])
    ax3.set_xlabel(OX_description, fontsize=14)
    ax3.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

# Results plot generation - buffer simulation v2
def print_buffer_simulations_v2():
    viridis(1.0, 0, 4)

    k1=10
    k2=1000

    domain = 'lambda'
    anti_domain_1 =  'plr_vo'
    anti_domain_2 =  'plr_c1'

    sim1_1_label = "AC_VO: K=10"
    sim1_2_label = "Class 1: K=10"
    sim1_3_label = "AC_VO: K=1000"
    sim1_4_label = "Class 1: K=1000"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/MSC/buff/lambda/buffLambda.csv', delimiter=',')

    OX_description = "Lambda"
    OY_description = "Packet loss ratio"
    result_file = 'results/MSC/buff/lambda/plrBuffLambda1.svg'

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1[sim1['buffer'] == k1].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_2_std = sim1[sim1['buffer'] == k1].groupby([domain]).std().loc[:,anti_domain_2]
    sim1_3_std = sim1[sim1['buffer'] == k2].groupby([domain]).std().loc[:,anti_domain_1]
    sim1_4_std = sim1[sim1['buffer'] == k2].groupby([domain]).std().loc[:, anti_domain_2]

    # Calculating number of probes
    sim1_1_n = sim1[sim1['buffer'] == k1].groupby([domain]).count().loc[:,anti_domain_1]
    sim1_2_n = sim1[sim1['buffer'] == k1].groupby([domain]).count().loc[:, anti_domain_2]
    sim1_3_n = sim1[sim1['buffer'] == k2].groupby([domain]).count().loc[:, anti_domain_1]
    sim1_4_n = sim1[sim1['buffer'] == k2].groupby([domain]).count().loc[:, anti_domain_2]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)
    sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)
    sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)

    # Results grouping
    sim1_1 = sim1[sim1['buffer'] == k1].groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim1[sim1['buffer'] == k1].groupby([domain])[anti_domain_2].mean()
    sim1_3 = sim1[sim1['buffer'] == k2].groupby([domain])[anti_domain_1].mean()
    sim1_4 = sim1[sim1['buffer'] == k2].groupby([domain])[anti_domain_2].mean()

    # Results plotting
    ax1_1 = sim1_1.plot(marker='x', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax1_2 = sim1_2.plot(ax=ax1_1, marker='o', legend=True,yerr=sim1_2_err,capsize=4)
    ax1_3 = sim1_3.plot(ax=ax1_2, marker='v', legend=True, yerr=sim1_3_err, capsize=4)
    ax1_4 = sim1_4.plot(ax=ax1_3, marker='*', legend=True, yerr=sim1_4_err, capsize=4,ylim=[0,1])

    # log scale option
    #ax4.set_xscale('log')

    ax1_4.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label])
    ax1_4.set_xlabel(OX_description, fontsize=14)
    ax1_4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

# Results plot generation - RTS simulation v1
def print_rts_simulations(m1,m2,m3,m4,label,file,file_in1,file_in2,lim,log_scale=False):
    viridis(1, 0, 4)

    domain = 'sync'
    anti_domain_1 =  m1
    anti_domain_2 =  m2
    anti_domain_3 =  m3
    anti_domain_4 =  m4

    sim1_1_label = "Wi-Fi AC_VO RTS ON"
    sim1_2_label = "Wi-Fi AC_VO RTS OFF"

    sim1_3_label = "NR-U Class 1 RTS ON"
    sim1_4_label = "NR-U Class 1 RTS OFF"

    # Simulation results parameters
    sim1 = pd.read_csv(file_in1, delimiter=',')
    sim2 = pd.read_csv(file_in2, delimiter=',')

    # 'Synchronization slot duration [\u03bcs]'
    OX_description = 'Synchronization slot duration [\u03bcs]'
    OY_description = label
    result_file = file

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1.groupby([domain]).std().loc[:, anti_domain_1]
    sim1_2_std = sim2.groupby([domain]).std().loc[:, anti_domain_2]

    sim1_3_std = sim1.groupby([domain]).std().loc[:, anti_domain_3]
    sim1_4_std = sim2.groupby([domain]).std().loc[:, anti_domain_4]

    # Calculating number of probes
    sim1_1_n = sim1.groupby([domain]).count().loc[:, anti_domain_1]
    sim1_2_n = sim2.groupby([domain]).count().loc[:, anti_domain_2]

    sim1_3_n = sim1.groupby([domain]).count().loc[:, anti_domain_3]
    sim1_4_n = sim2.groupby([domain]).count().loc[:, anti_domain_4]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)

    sim1_3_err = sim1_3_std / np.sqrt(sim1_3_n) * t.ppf(1 - alfa / 2, sim1_3_n - 1)
    sim1_4_err = sim1_4_std / np.sqrt(sim1_4_n) * t.ppf(1 - alfa / 2, sim1_4_n - 1)

    # Results grouping
    sim1_1 = sim1.groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim2.groupby([domain])[anti_domain_2].mean()

    sim1_3 = sim1.groupby([domain])[anti_domain_3].mean()
    sim1_4 = sim2.groupby([domain])[anti_domain_4].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='o', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4 )

    ax3 = sim1_3.plot(ax=ax2, marker='o', legend=True , mfc='none',yerr=sim1_3_err,capsize=4)
    ax4 = sim1_4.plot(ax=ax3, marker='o', legend=True,yerr=sim1_4_err,capsize=4,ylim=lim)
    ax4.xaxis.set_major_locator(MaxNLocator(integer=True))

    # log scale option
    if log_scale:
        ax4.set_xscale('log')

    ax4.legend([sim1_1_label, sim1_2_label, sim1_3_label, sim1_4_label])
    ax4.set_xlabel(OX_description,fontsize=14)
    ax4.set_ylabel(OY_description,fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

# Results plot generation - RTS simulation v2 (JFI)
def print_rts_simulations_v2(m1,label,file,file_in1,file_in2,lim,log_scale=False):
    viridis(1, 0, 4)

    domain = 'sync'
    anti_domain_1 =  m1

    sim1_1_label = "RTS ON"
    sim1_2_label = "RTS OFF"

    # Simulation results parameters
    sim1 = pd.read_csv(file_in1, delimiter=',')
    sim2 = pd.read_csv(file_in2, delimiter=',')

    # 'Synchronization slot duration [\u03bcs]'
    OX_description = 'Synchronization slot duration [\u03bcs]'
    OY_description = label
    result_file = file

    # t-student parameter for confidence intervals
    alfa = 0.05

    # Calculating standard deviation
    sim1_1_std = sim1.groupby([domain]).std().loc[:, anti_domain_1]
    sim1_2_std = sim2.groupby([domain]).std().loc[:, anti_domain_1]

    # Calculating number of probes
    sim1_1_n = sim1.groupby([domain]).count().loc[:, anti_domain_1]
    sim1_2_n = sim2.groupby([domain]).count().loc[:, anti_domain_1]

    # Calculating error for each probe
    sim1_1_err = sim1_1_std / np.sqrt(sim1_1_n) * t.ppf(1 - alfa / 2, sim1_1_n - 1)
    sim1_2_err = sim1_2_std / np.sqrt(sim1_2_n) * t.ppf(1 - alfa / 2, sim1_2_n - 1)

    # Results grouping
    sim1_1 = sim1.groupby([domain])[anti_domain_1].mean()
    sim1_2 = sim2.groupby([domain])[anti_domain_1].mean()

    # Results plotting
    ax1 = sim1_1.plot(marker='o', legend=True, mfc='none',yerr=sim1_1_err,capsize=4)
    ax2 = sim1_2.plot(ax=ax1, marker='o', legend=True,yerr=sim1_2_err,capsize=4,ylim=lim)

    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

    # log scale option
    if log_scale:
        ax2.set_xscale('log')

    ax2.legend([sim1_1_label, sim1_2_label])
    ax2.set_xlabel(OX_description,fontsize=14)
    ax2.set_ylabel(OY_description,fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

if __name__ == "__main__":

    # Results plot generation - standard simulations
    print_four_simulations(domain='tx_skipped',m1='airtime_be',m2='airtime_c3',m3='airtime_be',m4='airtime_c3',label="Channel occupancy",file="results/MSC/skip/cot_skip_2.svg",file_in='csvresults/MSC/skip/skip_2.csv',lim=[0,1],log_scale=False)
    plt.clf()
    print_four_simulations(domain='tx_skipped',m1='latency_be',m2='latency_c3',m3='latency_be',m4='latency_c3',label="Latency [s]",file="results/MSC/skip/lat_skip_2.svg",file_in='csvresults/MSC/skip/skip_2.csv',lim=[0,1],log_scale=False)
    plt.clf()
    #print_four_simulations('jitter_vi','jitter_c2','jitter_bk','jitter_c4',"Jitter [s]","results/MSC/buff/size/jitBuffSize2.svg",'csvresults/MSC/buff/size/buffSize2.csv',lim=[0,1000],log_scale=False)
    plt.clf()
    print_four_simulations(domain='tx_skipped',m1='plr_be',m2='plr_c3',m3='plr_be',m4='plr_c3',label="Packet loss ratio",file="results/MSC/skip/plr_skip_2.svg",file_in='csvresults/MSC/skip/skip_2.csv',lim=[0,1],log_scale=False)

    # Results plot generation - buffer simulation v1
    #print_buffer_simulations()

    # Results plot generation - buffer simulation v2
    #print_buffer_simulations_v2()

    # Results plot generation - rts simulation v1
    #print_rts_simulations('airtime_vo','airtime_vo','airtime_c1','airtime_c1',"Channel occupancy","results/MSC/rts/sync/rts_sync_1_cot.svg",'csvresults/MSC/rts/rts_1_ON.csv','csvresults/MSC/rts/rts_1_OFF.csv',[0,1],True)
    #print_rts_simulations('latency_vo', 'latency_vo', 'latency_c1', 'latency_c1', "Latency [s]","results/MSC/rts/sync/rts_sync_1_lat.svg", 'csvresults/MSC/rts/rts_1_ON.csv','csvresults/MSC/rts/rts_1_OFF.csv', [0, 25], True)

    # Results plot generation - rts simulation v2
    #print_rts_simulations_v2('JainFairIndex', "Jain's fairness index","results/MSC/rts/sync/rts_sync_2_jfi.svg", 'csvresults/MSC/rts/rts_2_ON.csv','csvresults/MSC/rts/rts_2_OFF.csv', [0, 1], True)




