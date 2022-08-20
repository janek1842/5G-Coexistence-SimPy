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

# Old validations (first version)
def viridis(a, b, color_amount):
    color = mpl.cm.viridis(np.linspace(a, b, n))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)

def print_collision_prob():
    # read data from csv

    viridis(0.3, 1.0, 2)

    data = pd.read_csv('results.csv', delimiter=',')
    data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data = data.groupby(['Stations'])['Colisions'].mean()
    data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax = data.plot(title='5G_Coexistance vs DCF simulators', marker='o', legend=True, ylim=(0, 40))
    # DCF - PT
    ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    ax2.legend(['5G-Coex-SimPy', 'DCF-SimPy'])
    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/colisonProbability.png')

def print_airtime_34():
    # read data from csv
    viridis(0.0, 1.0, 4)

    data = pd.read_csv('output_test.csv', delimiter=',')
    data_dcf = pd.read_csv('output_test.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Stations'])['ChannelOccupancy'].mean()
    data3 = data.groupby(['Stations'])['ChannelEfficiency'].mean()

    data2dcf = data_dcf.groupby(['Stations'])['Occupancy'].mean()
    data3dcf = data_dcf.groupby(['Stations'])['Efficiency'].mean()
    # data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax = data2.plot( marker='o', legend=True, ylim=(0, 1))
    ax2 = data3.plot( marker='o', legend=True, ylim=(0, 1))

    ax3 = data2dcf.plot( marker='x', legend=True, ylim=(0, 1), linestyle= '--')
    ax4 = data3dcf.plot( marker='x', legend=True, ylim=(0, 1), linestyle= '--')

    ax2.legend(['5G-Coex-SimPy occupancy', '5G-Coex-SimPy efficiency', 'DCF-SimPy occupancy', 'DCF-SimPy efficiency' ])
    ax2.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax2.set_ylabel('Normalized airtime', fontsize=14)

    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('results/airtime_efficiency_and_occupancy2.png')

def print_channel_occupancy():
    viridis(0.2, 1.0, 2)

    # read data from csv
    data = pd.read_csv('output_test.csv', delimiter=',')
    data_dcf = pd.read_csv('output_test.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Stations'])['ChannelOccupancy'].mean()
    data2dcf = data_dcf.groupby(['Stations'])['Occupancy'].mean()
    # plotting
    # 5G _ JC
    ax = data2.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='o', legend=True, ylim=(0, 1))


    #ax2.legend(['Normalized Channel Occupancy', 'Channel Efficiency'])

    ax3 = data2dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1), linestyle= '--')


    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Channel occupancy time', fontsize=14)
    ax3.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax3.set_ylabel('Channel occupancy time', fontsize=14)

    ax3.legend(['5G-Coex-SimPy occupancy', 'DCF-SimPy occupancy'])
    # Save to file
    plt.tight_layout()
    plt.savefig('results/channel_occupancy.png')

def print_channel_efficency():
    viridis(0.2, 1.0, 2)

    # read data from csv
    data = pd.read_csv('output_test.csv', delimiter=',')
    data_dcf = pd.read_csv('output_test.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data3 = data.groupby(['Stations'])['ChannelEfficiency'].mean()
    data3dcf = data_dcf.groupby(['Stations'])['Efficiency'].mean()
    # data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax2 = data3.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='o', legend=True, ylim=(0, 1))
    ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")

    ax4 = data3dcf.plot(title='Airtime 5G-Coexistance-Simpy vs DCF-Simpy', marker='x', legend=True, ylim=(0, 1), linestyle= '--')

    ax4.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Normalized airtime")
    ax2.legend(['5G-Coex-SimPy efficiency','DCF-SimPy efficiency'])

    ax2.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax2.set_ylabel('Channel efficiency time', fontsize=14)
    ax4.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax4.set_ylabel('Channel efficiency time', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/channel_efficiency.png')

def print_airtime_norm_per_station():
    viridis(0.5, 1.0, 10)
    # read data from csv
    data = pd.read_csv('airtime12_new2.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Num'])['NormPerStation'].mean()

    # plotting
    # 5G _ JC
    ax = data2.plot.bar(title='Per station normalized airtime', legend=False, ylim=(0, 1))
    #ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Mean normalized airtime', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/normalized_airtime_per_station.png')

def print_airtime_per_station():
    viridis(0.0, 1.0, 10)
    # read data from csv
    data = pd.read_csv('airtime12_new2.csv', delimiter=',')
    # data2 = pd.read_csv('results2.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data2 = data.groupby(['Num'])['PerStation'].mean()

    # plotting
    # 5G _ JC
    ax = data2.plot.bar(title='Per station airtime', legend=False, ylim=(0, 100))
    #ax.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="% of time")
    ax.set_xlabel('Number of transmitting Wi-Fi stations', fontsize=14)
    ax.set_ylabel('Mean airtime', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/airtime_per_station.png')

def print_nru_airtime():
    # read data from csv
    viridis(0.0, 1.0, 2)

    data = pd.read_csv('nru_airtime_good.csv', delimiter=',')


    # group by number of stations and calculate mean colision proob
    #data2 = data.groupby(['Gnb'])['ChannelOccupancy'].mean()
    data3 = data.groupby(['Gnb'])['ChannelEfficiency'].mean()




    # plotting
    # 5G _ JC
    #ax = data2.plot(title='NR-U airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data3.plot(title='NR-U airtime', marker='x', legend=True, ylim=(0, 1))


    data2 = pd.read_csv('lbt_good.csv', delimiter=',')
    data4 = data2.groupby(['Gnb'])['ChannelEfficiency'].mean()
    ax3 = data4.plot(title='NR-U airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')

    #ax3.legend(['5G-Coex-SimPy occupancy', '5G-Coex-SimPy efficiency', 'NRU-SimPy'])
    ax3.legend(['5G-Coex-SimPy', 'NRU-SimPy'])
    ax3.set_xlabel('Number of transmitting gNBs', fontsize=14)
    ax3.set_ylabel('Efficiency', fontsize=14)

    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('results/nru_airtime_good2.png')

def print_collision_prob_NRU():
    # read data from csv

    viridis(0.0, 1.0, 2)

    data = pd.read_csv('nru_colision_good.csv', delimiter=',')
    data2 = pd.read_csv('lbt_colision.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data = data.groupby(['Stations'])['Colisions'].mean()
    data2 = data2.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax = data.plot(title='5G_Coexistance vs NRU-MZ', marker='o', legend=True, ylim=(0, 60))
    # DCF - PT
    ax2 = data2.plot(title='5G_Coexistance vs NRU-MZ', marker='x', legend=True, ylim=(0, 60), linestyle= '--')
    ax2.legend(['5G-Coex-SimPy',  'NRU-SimPy'])
    ax.set_xlabel('Number of transmitting gNBs', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/colisonProbability_NRU_good.png')

def print_collision_prob_NRU_gap():
    # read data from csv

    viridis(0.0, 1.0, 2)

    data = pd.read_csv('nru_colision_gap.csv', delimiter=',')


    # group by number of stations and calculate mean colision proob
    data = data.groupby(['Stations'])['Colisions'].mean()

    # plotting
    # 5G _ JC
    ax = data.plot(title='5G_Coexistance vs NRU-MZ', marker='o', legend=True, ylim=(0, 60))
    # DCF - PT
    ax.legend(['5G-Coex-SimPy- gap'])
    ax.set_xlabel('Number of transmitting gNBs', fontsize=14)
    ax.set_ylabel('Collision probability', fontsize=14)

    # Save to file
    plt.tight_layout()
    plt.savefig('results/colisonProbability_NRU_gap.png')

def print_nru_airtime_gap():
    # read data from csv
    viridis(0.0, 1.0, 3)

    data = pd.read_csv('nru_airtime_gap5.csv', delimiter=',')

    # group by number of stations and calculate mean colision proob
    data3 = data.groupby(['Gnb'])['ChannelEfficiency'].mean()

    # plotting
    # 5G _ JC
    ax2 = data3.plot(title='NR-U gap airtime', marker='o', legend=True, ylim=(0.8, 1))


    data2 = pd.read_csv('lbt_gap2.csv', delimiter=',')
    data4 = data2.groupby(['Gnb'])['ChannelEfficiency'].mean()
    ax3 = data4.plot(title='NR-U airtime', marker='x', legend=True, ylim=(0.8, 1), linestyle='--')

    ax2.legend(['5G-Coex-SimPy',  'NRU-SimPy'])

    matlab = pd.read_csv('matlab.csv', delimiter=',')
    matalb2 = matlab.groupby(['Gnb'])['ChannelEfficiency'].mean()
    ax4 = matalb2.plot(title='NR-U airtime', marker='x', legend=True, ylim=(0.8, 1), linestyle='--')



    ax2.legend(['5G-Coex-SimPy', 'NRU-SimPy', 'Matlab'])
    ax2.set_xlabel('Number of transmitting gNBs', fontsize=14)
    ax2.set_ylabel('Efficiency', fontsize=14)


    # # DCF - PT
    # ax2 = data2.plot(title='5G_Coexistance vs DCF simulators', marker='x', legend=True, ylim=(0, 40))
    # ax2.set(xlabel="Number of transmitting Wi-Fi stations", ylabel="Collision probability")
    # ax2.legend(['5G-Coexistance-Simpy', 'DCF-Simpy'])

    # Save to file
    plt.tight_layout()
    plt.savefig('results/nru_airtime_gap7.png')

def print_coexistance_airtime():
    # read data from csv
    viridis(0.0, 1.0, 2)

    data = pd.read_csv('matlab_results.csv', delimiter=',')
    # group by number of stations and calculate mean colision proob
    data3 = data.groupby(['nNR'])['cotWifi'].mean()
    data2 = data.groupby(['nNR'])['cotNR'].mean()

    # plotting
    ax = data2.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data3.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1))

    ax2.legend(['cotNR',  'cotWifi'])

    ax2.set_xlabel('Number of Wifi/NR nodes', fontsize=14)
    ax2.set_ylabel('Channel occupancy time', fontsize=14)
    # Save to file
    plt.tight_layout()
    plt.savefig('results/coex_airtime.png')

def print_coexistance_airtime_my():
    # read data from csv
    viridis(0.0, 1.0, 2)

    data = pd.read_csv('coex_gnb_test.csv', delimiter=',')
    # group by number of stations and calculate mean colision proob
    data3 = data.groupby(['nNR'])['cotWifi'].mean()
    data2 = data.groupby(['nNR'])['cotNR'].mean()

    # plotting
    ax = data2.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data3.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1))

    ax2.legend(['cotNR',  'cotWifi'])

    ax2.set_xlabel('Number of Wifi/NR nodes', fontsize=14)
    ax2.set_ylabel('Channel occupancy time', fontsize=14)
    # Save to file
    plt.tight_layout()
    plt.savefig('results/coex_airtime.png')

# My validations

def valid_two_simulations():
    viridis(0.0, 1.0, 2)

    # Simulation results parameters
    domain = 'sync'
    anti_domain = 'ChannelEfficiencyNR'

    sim1_label = "MATLAB"
    sim2_label = "5G-Coex-SimPy"

    sim1 = pd.read_csv('csvresults/VAL/NRu-gap/slot/matlab-slot-v20.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/VAL/NRu-gap/slot/sp-slot-v2.csv', delimiter=',')

    x_axis_description = "Synchronization slot duration [\u03bcs]"
    y_axis_description = "Channel efficiency"

    sim1_color = "black"
    sim2_color = "red"

    y_range = (0,1)
    result_file_path = 'results/VAL/NRu-gap/slot/eff/eff-slot-v2.svg'

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
    sim1_plot = sim1.plot(marker='o', legend=True, capsize=4, yerr = sim1_err, color = sim1_color,ylim=y_range, mfc='none')
    sim2_plot = sim2.plot(ax=sim1_plot, marker='x', legend=True, capsize=4, yerr = sim2_err, color = sim2_color)
    sim1_plot.set_xscale('log')

    sim2_plot.legend([sim1_label,sim2_label])
    sim2_plot.set_xlabel(x_axis_description, fontsize=14)
    sim2_plot.set_ylabel(y_axis_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file_path)

def valid_four_simulations():
    viridis(0.0, 1.0, 2)

    domain = 'sync'
    anti_domain_1 = 'ChannelEfficiencyNR'
    anti_domain_2 = 'ChannelEfficiencyWiFi'

    sim1_1_label = "MATLAB: NR-U"
    sim1_2_label = "MATLAB: WiFi"
    sim2_1_label = "5G-Coex-SimPy: NR-U"
    sim2_2_label = "5G-Coex-SimPy: WiFi"

    # Simulation results parameters
    sim1 = pd.read_csv('csvresults/VAL/Coex/slot/matlab-slot-v2.csv', delimiter=',')
    sim2 = pd.read_csv('csvresults/VAL/Coex/slot/slot-v2.csv', delimiter=',')

    OX_description = "Synchronization slot duration [\u03bcs]"
    OY_description = "Channel efficiency"
    result_file='results/VAL/Coex/slot/eff-slot-v2.svg'

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
    ax1 = sim1_1.plot(marker='x', legend=True,yerr=sim1_1_err,capsize=4,ylim=(0,1),color='green')
    ax2 = sim1_2.plot(ax=ax1, marker='x', legend=True,yerr=sim1_2_err,capsize=4,color='orange')
    ax3 = sim2_1.plot(ax=ax2,marker='o', legend=True,yerr=sim2_1_err,capsize=4,color='red',mfc='none')
    ax4 = sim2_2.plot(ax=ax3, marker='o', legend=True,yerr=sim2_2_err,capsize=4,mfc='none')

    # log scale option
    ax4.set_xscale('log')

    ax4.legend([sim1_1_label,sim1_2_label,sim2_1_label,sim2_2_label])
    ax4.set_xlabel(OX_description, fontsize=14)
    ax4.set_ylabel(OY_description, fontsize=14)

    plt.tight_layout()
    plt.savefig(result_file)

if __name__ == "__main__":
    valid_four_simulations()
    #valid_two_simulations()




