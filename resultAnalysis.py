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


def print_coex():

    viridis(0.0, 1.0, 4)

    data_my = pd.read_csv('output_test.csv', delimiter=',')

    data_my_wifi = data_my.groupby(['Gnb'])['ChannelOccupancy'].mean()
    data_my_gnb = data_my.groupby(['Gnb'])['ChannelOccupancyNR'].mean()

    data_matlab = pd.read_csv('coex_rs_wifi22.csv', delimiter=',')

    data_matlab_wifi = data_matlab.groupby(['nWifi'])['cotWifi'].mean()
    data_matlab_gnb = data_matlab.groupby(['nWifi'])['cotLAA'].mean()

    ax1 = data_my_wifi.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data_my_gnb.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax1 = data_matlab_wifi.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')
    ax2 = data_matlab_gnb.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')

    ax2.legend(['Coex_wifi', 'Coex_gnb', 'Matlab_wifi', 'Matalb_gnb'])
    ax2.set_xlabel('Number of Wifi/NR nodes', fontsize=14)
    ax2.set_ylabel('Channel occupancy time', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/coex_comparison_rs2.png')

def print_matlab():

    viridis(0.0, 1.0, 4)

    data_matlab = pd.read_csv('coex_matlab4.csv', delimiter=',')

    data_matlab_wifi = data_matlab.groupby(['nWifi'])['cotWifi'].mean()
    data_matlab_gnb = data_matlab.groupby(['nWifi'])['cotLAA'].mean()

    ax1 = data_matlab_wifi.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data_matlab_gnb.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))

    ax2.legend(['Matlab_wifi', 'Matalb_gnb'])
    ax2.set_xlabel('Number of Wifi/NR nodes', fontsize=14)
    ax2.set_ylabel('Channel occupancy time', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/coex_comparison2.png')

def print_coex_gap():

    viridis(0.0, 1.0, 4)

    data_my = pd.read_csv('coex_gnbOnly.csv', delimiter=',')

    # data_my_wifi = data_my.groupby(['Gnb'])['ChannelOccupancy'].mean()
    data_my_gnb = data_my.groupby(['Gnb'])['ChannelOccupancyNR'].mean()

    data_matlab = pd.read_csv('coex_tylko_gap.csv', delimiter=',')

    # data_matlab_wifi = data_matlab.groupby(['nWifi'])['cotWifi'].mean()
    data_matlab_gnb = data_matlab.groupby(['nNR'])['cotNR'].mean()

    # ax1 = data_my_wifi.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data_my_gnb.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    # ax1 = data_matlab_wifi.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')
    ax2 = data_matlab_gnb.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')

    ax2.legend(['Coex_gnb', 'Matalb_gnb'])
    ax2.set_xlabel('Number of Wifi/NR nodes', fontsize=14)
    ax2.set_ylabel('Channel occupancy time', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/coex_compa_gap.png')

def print_coex_gap_matlab():
    viridis(0.0, 1.0, 4)

    data_my = pd.read_csv('coex_gnb_wifi4.csv', delimiter=',')

    data_my_wifi = data_my.groupby(['Gnb'])['ChannelOccupancy'].mean()
    data_my_gnb = data_my.groupby(['Gnb'])['ChannelOccupancyNR'].mean()

    data_matlab = pd.read_csv('coex_gap_wifi.csv', delimiter=',')

    data_matlab_wifi = data_matlab.groupby(['nWifi'])['cotWifi'].mean()
    data_matlab_gnb = data_matlab.groupby(['nWifi'])['cotNR'].mean()

    ax1 = data_my_wifi.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax2 = data_my_gnb.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax1 = data_matlab_wifi.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')
    ax2 = data_matlab_gnb.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')

    ax2.legend(['Coex_wifi', 'Coex_gnb', 'Matlab_wifi', 'Matalb_gnb'])
    ax2.set_xlabel('Number of Wifi/NR nodes', fontsize=14)
    ax2.set_ylabel('Channel occupancy time', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/coex_comparison_gap3.png')

def valid_wifi():
    viridis(0.0, 1.0, 2)

    dcf = pd.read_csv('da/dcf_wifi.csv', delimiter=',')
    matlab = pd.read_csv('da/matlab_wifi.csv', delimiter=',')

    dcf2 = dcf.groupby(['WiFi'])['ChannelOccupancy'].mean()
    #data_my_gnb = data_my.groupby(['Gnb'])['ChannelOccupancyNR'].mean()

    data_my2 = pd.read_csv('valid_wifi.csv', delimiter=',')

    rs = data_my.groupby(['Gnb'])['ChannelOccupancy'].mean()

    data_my3 = pd.read_csv('valid_wifi.csv', delimiter=',')

    gap = data_my.groupby(['Gnb'])['ChannelOccupancy'].mean()


    data_matlab = pd.read_csv('coex_gap_wifi.csv', delimiter=',')

    data_matlab_wifi = data_matlab.groupby(['nWifi'])['cotWifi'].mean()
    data_matlab_gnb = data_matlab.groupby(['nWifi'])['cotNR'].mean()

    ax1 = wifi.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    #ax2 = data_my_gnb.plot(title='Coexistance airtime', marker='o', legend=True, ylim=(0, 1))
    ax1 = data_matlab_wifi.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')
    ax2 = data_matlab_gnb.plot(title='Coexistance airtime', marker='x', legend=True, ylim=(0, 1), linestyle='--')

    ax2.legend(['Coex_wifi', 'Coex_gnb', 'Matlab_wifi', 'Matalb_gnb'])
    ax2.set_xlabel('Number of Wifi/NR nodes', fontsize=14)
    ax2.set_ylabel('Channel occupancy time', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/coex_comparison_gap3.png')

def valid_throughput():
    viridis(0.0, 1.0, 2)

    throughput = pd.read_csv('csvresults/OTHERS/results_throguhput_wifi.csv', delimiter=',')
    ns3 = pd.read_csv('csvresults/NS3/ns3_throughput_results.csv', delimiter=',')

    #matlab = pd.read_csv('da/matlab_wifi.csv', delimiter=',')
    alfa = 0.05

    thr_std = throughput.groupby(['WiFi'])['Throughput'].std()
    ns3_std = ns3.groupby(['WiFi'])['Throughput'].std()

    thr_n = throughput.groupby(['WiFi'])['Throughput'].count().iloc[1]
    ns3_n = ns3.groupby(['WiFi'])['Throughput'].count().iloc[1]

    thr_err = thr_std / math.sqrt(thr_n) * t.ppf(1-alfa/2,thr_n-1)
    ns3_err = ns3_std / math.sqrt(ns3_n) * t.ppf(1-alfa/2,ns3_n-1)

    throughput = throughput.groupby(['WiFi'])['Throughput'].mean()
    ns3 = ns3.groupby(['WiFi'])['Throughput'].mean()

    ax1 = throughput.plot(marker='o', legend=True, ylim=(0, 40),yerr = thr_err,capsize=4)
    ax2 = ns3.plot(marker='x', legend=True, ylim=(0, 40),yerr = ns3_err,capsize=4)

    ax1.legend(['Coex_wifi_v2',"ns-3"])
    ax1.set_xlabel('Total number of stations', fontsize=14)
    ax1.set_ylabel('Aggregated throughput [Mb/s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/THRPT/results_throughput_wifi.svg')

def valid_throughput_and_size():
    viridis(0.0, 1.0, 2)

    throughput = pd.read_csv('csvresults/OTHERS/results_throguhput_payload.csv', delimiter=',')
    ns3 = pd.read_csv('csvresults/NS3/ns3_throughput_size.csv', delimiter=',')

    #matlab = pd.read_csv('da/matlab_wifi.csv', delimiter=',')

    alfa = 0.05

    thr_std = throughput.groupby(['Payload'])['Throughput'].std()
    ns3_std = ns3.groupby(['Payload'])['Throughput'].std()

    thr_n = throughput.groupby(['Payload'])['Throughput'].count().iloc[1]
    ns3_n = ns3.groupby(['Payload'])['Throughput'].count().iloc[1]

    thr_err = thr_std / math.sqrt(thr_n) * t.ppf(1 - alfa / 2, thr_n - 1)
    ns3_err = ns3_std / math.sqrt(ns3_n) * t.ppf(1 - alfa / 2, ns3_n - 1)

    throughput = throughput.groupby(['Payload'])['Throughput'].mean()
    ns3 = ns3.groupby(['Payload'])['Throughput'].mean()

    ax1 = throughput.plot(marker='o', legend=True, ylim=(0, 40),yerr = thr_err,capsize=5)
    ax2 = ns3.plot(marker='x', legend=True, ylim=(0, 40),yerr = ns3_err,capsize=5)

    ax1.legend(['Coex_wifi_v2',"ns-3"])
    ax1.set_xlabel('Payload size [B]', fontsize=14)
    ax1.set_ylabel('Aggregated throughput [Mb/s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/THRPT/results_throughput_size.svg')

def valid_fair_index():
    viridis(0.0, 1.0, 2)

    throughput = pd.read_csv('csvresults/OTHERS/jain_fairness.csv', delimiter=',')

    throughput = throughput.groupby(['SimulationTime'])['JainFairIndex'].mean()

    ax1 = throughput.plot(marker='o', legend=True, ylim=(0.92, 1))

    ax1.legend(['Coex_wifi_v2'])
    ax1.set_xlabel('Simulation time [s]', fontsize=14)
    ax1.set_ylabel('Jain\'s fairness index', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/OTHERS/jain_fairness_index.svg')

def valid_airtime_data():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/EDCA/edca_simulation_v1.csv', delimiter=',')

    airtime_be = edca.groupby(['WiFi'])['beAirTime'].mean() / (10*1000000)
    airtime_bg = edca.groupby(['WiFi'])['bgAirTime'].mean() / (10*1000000)
    airtime_vd = edca.groupby(['WiFi'])['vdAirTime'].mean() / (10*1000000)
    airtime_vo = edca.groupby(['WiFi'])['vcAirTime'].mean() / (10*1000000)

    ax1 = airtime_be.plot(marker='o', legend=True)
    ax2 = airtime_bg.plot(ax=ax1,marker='o', legend=True)
    ax3 = airtime_vd.plot(ax=ax2,marker='o', legend=True)
    ax4 = airtime_vo.plot(ax=ax3,marker='o', legend=True)

    ax4.legend(['BestEffort',"Background","Video","Voice"])
    ax4.set_xlabel('Total number of stations', fontsize=14)
    ax4.set_ylabel('Normalized airtime [s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/EDCA/edca_simulations_saturated.png')

def valid_airtime_data():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/EDCA/edca_simulation_v8.csv', delimiter=',')

    airtime_be = edca.groupby(['WiFi'])['beAirTime'].mean() / (10*1000000)
    airtime_bg = edca.groupby(['WiFi'])['bgAirTime'].mean() / (10*1000000)
    airtime_vd = edca.groupby(['WiFi'])['vdAirTime'].mean() / (10*1000000)
    airtime_vo = edca.groupby(['WiFi'])['vcAirTime'].mean() / (10*1000000)

    ax1 = airtime_be.plot(marker='o', legend=True)
    ax2 = airtime_bg.plot(ax=ax1,marker='o', legend=True)
    ax3 = airtime_vd.plot(ax=ax2,marker='o', legend=True)
    ax4 = airtime_vo.plot(ax=ax3,marker='o', legend=True)

    ax4.legend(['BestEffort',"Background","Video","Voice"])
    ax4.set_xlabel('Total number of stations', fontsize=14)
    ax4.set_ylabel('Normalized airtime [s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/EDCA/edca_saturated_v5.svg')

def valid_thrpt_data_with_ns3_vcAndvd():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/EDCA/edca_simulation_v9.csv', delimiter=',')
    ns3 = pd.read_csv('csvresults/NS3/ns3_edca.csv', delimiter=',')

    alfa = 0.05
    thr_std_vd = edca.groupby(['WiFi'])['thrpt_vd'].std()
    thr_std_vc = edca.groupby(['WiFi'])['thrpt_vc'].std()

    ns3_std_vd = ns3.groupby(['WiFi'])['thrpt_vd'].std()
    ns3_std_vc = ns3.groupby(['WiFi'])['thrpt_vc'].std()

    thr_n_vc = edca.groupby(['WiFi'])['thrpt_vc'].count().iloc[1]
    thr_n_vd = edca.groupby(['WiFi'])['thrpt_vd'].count().iloc[1]

    ns3_n_vc = ns3.groupby(['WiFi'])['thrpt_vc'].count().iloc[1]
    ns3_n_vd = ns3.groupby(['WiFi'])['thrpt_vd'].count().iloc[1]

    thr_err_vc = thr_std_vc / math.sqrt(thr_n_vc) * t.ppf(1 - alfa / 2, thr_n_vc - 1)
    thr_err_vd = thr_std_vd / math.sqrt(thr_n_vd) * t.ppf(1 - alfa / 2, thr_n_vd - 1)

    ns3_err_vc = ns3_std_vc / math.sqrt(ns3_n_vc) * t.ppf(1 - alfa / 2, ns3_n_vc - 1)
    ns3_err_vd = ns3_std_vd / math.sqrt(ns3_n_vd) * t.ppf(1 - alfa / 2, ns3_n_vd - 1)

    thrpt_vd = edca.groupby(['WiFi'])['thrpt_vd'].mean()
    thrpt_vo = edca.groupby(['WiFi'])['thrpt_vc'].mean()

    thrpt_ns3_vd = ns3.groupby(['WiFi'])['thrpt_vd'].mean()
    thrpt_ns3_vc = ns3.groupby(['WiFi'])['thrpt_vc'].mean()

    ax1 = thrpt_vd.plot(marker='o', legend=True,yerr=thr_err_vd,capsize=4)
    ax2 = thrpt_vo.plot(ax=ax1, marker='o', legend=True,yerr=thr_err_vc,capsize=4)

    ax3 = thrpt_ns3_vd.plot(ax=ax2,marker='o', legend=True,yerr=ns3_err_vd,capsize=4)
    ax4 = thrpt_ns3_vc.plot(ax=ax3, marker='o', legend=True,yerr=ns3_err_vc,capsize=4)

    ax4.legend(["coex_v2_video", "coex_v2_voice","ns3_video","ns3_voice"])
    ax4.set_xlabel('Total number of stations', fontsize=14)
    ax4.set_ylabel('Aggregated throughput [Mb/s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/EDCA/edca_simulations_validated.svg')

def valid_thrpt_data_with_ns3_bgAndbe():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/EDCA/edca_simulation_v9.csv', delimiter=',')
    ns3 = pd.read_csv('csvresults/NS3/ns3_edca.csv', delimiter=',')

    alfa = 0.05
    thr_std_be = edca.groupby(['WiFi'])['thrpt_be'].std()
    thr_std_bg = edca.groupby(['WiFi'])['thrpt_bg'].std()

    ns3_std_be = ns3.groupby(['WiFi'])['thrpt_be'].std()
    ns3_std_bg = ns3.groupby(['WiFi'])['thrpt_bg'].std()

    thr_n_be = edca.groupby(['WiFi'])['thrpt_be'].count().iloc[1]
    thr_n_bg = edca.groupby(['WiFi'])['thrpt_bg'].count().iloc[1]

    ns3_n_be = ns3.groupby(['WiFi'])['thrpt_be'].count().iloc[1]
    ns3_n_bg = ns3.groupby(['WiFi'])['thrpt_bg'].count().iloc[1]

    thr_err_be = thr_std_be / math.sqrt(thr_n_be) * t.ppf(1 - alfa / 2, thr_n_be - 1)
    thr_err_bg = thr_std_bg / math.sqrt(thr_n_bg) * t.ppf(1 - alfa / 2, thr_n_bg - 1)

    ns3_err_be = ns3_std_be / math.sqrt(ns3_n_be) * t.ppf(1 - alfa / 2, ns3_n_be - 1)
    ns3_err_bg = ns3_std_bg / math.sqrt(ns3_n_bg) * t.ppf(1 - alfa / 2, ns3_n_bg - 1)

    thrpt_be = edca.groupby(['WiFi'])['thrpt_be'].mean()
    thrpt_bg = edca.groupby(['WiFi'])['thrpt_bg'].mean()

    thrpt_ns3_be = ns3.groupby(['WiFi'])['thrpt_be'].mean()
    thrpt_ns3_bg = ns3.groupby(['WiFi'])['thrpt_bg'].mean()

    ax1 = thrpt_be.plot(marker='o', legend=True,yerr=thr_err_be,capsize=4)
    ax2 = thrpt_bg.plot(ax=ax1, marker='o', legend=True,yerr=thr_err_bg,capsize=4)

    ax3 = thrpt_ns3_be.plot(ax=ax2,marker='o', legend=True,yerr=ns3_err_be,capsize=4)
    ax4 = thrpt_ns3_bg.plot(ax=ax3, marker='o', legend=True,yerr=ns3_err_bg,capsize=4)

    ax4.legend(["coex_v2_be", "coex_v2_bg","ns3_be","ns3_bg"])
    ax4.set_xlabel('Total number of stations', fontsize=14)
    ax4.set_ylabel('Aggregated throughput [Mb/s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/EDCA/edca_simulations_validated_p2.svg')

def valid_poisson_airtime():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/EDCA/edca_simulation_v2.csv', delimiter=',')

    airtime_be = edca.groupby(['lambda'])['beAirTime'].mean() / (10*1000000)

    ax4 = airtime_be.plot(marker='o', legend=True)

    ax4.legend(['Coex_wifi_v2'])
    ax4.set_xlabel('Per-station traffic intensity [packets/ms]', fontsize=14)
    ax4.set_ylabel('Normalized airtime [s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/EDCA/edca_simulations_v2.png')

def valid_poisson_airtime_peak():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/EDCA/peak_simulation.csv', delimiter=',')

    airtime_be = edca.groupby(['lambda'])['beAirTime'].mean()  / 1000000

    ax4 = airtime_be.plot(marker='o', legend=True)

    ax4.legend(['Coex_wifi_v2'])
    ax4.set_xlabel('Per-station traffic intensity [packets/ms]', fontsize=14)
    ax4.set_ylabel('Normalized airtime [s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/edca/edca_simulations_v3.png')

def valid_airtime_data_v2():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/EDCA/edca_simulation_v7.csv', delimiter=',')

    airtime_be = edca.groupby(['lambda'])['beAirTime'].mean() / (10*1000000)
    airtime_bg = edca.groupby(['lambda'])['bgAirTime'].mean() / (10*1000000)
    airtime_vd = edca.groupby(['lambda'])['vdAirTime'].mean() / (10*1000000)
    airtime_vo = edca.groupby(['lambda'])['vcAirTime'].mean() / (10*1000000)

    ax1 = airtime_be.plot(marker='o', legend=True)
    ax2 = airtime_bg.plot(ax=ax1,marker='o', legend=True)
    ax3 = airtime_vd.plot(ax=ax2,marker='o', legend=True)
    ax4 = airtime_vo.plot(ax=ax3,marker='o', legend=True)

    ax4.legend(['BestEffort',"Background","Video","Voice"])
    ax4.set_xlabel('Per-station traffic intensity [packets/ms]', fontsize=14)
    ax4.set_ylabel('Normalized airtime [s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/EDCA/edca_saturated_v4.svg')

def valid_lambda_with_ns3():
    viridis(0.0, 1.0, 2)

    edca = pd.read_csv('csvresults/LAMBDA/lambda_simulation_v1.csv', delimiter=',')
    ns3_1 = pd.read_csv('csvresults/NS3/ns3_lambda.csv', delimiter=',')

    airtime_be = edca.groupby(['lambda'])['Throughput'].mean()
    ns3 = ns3_1.groupby(['lambda'])['thrpt'].mean()

    alfa = 0.05

    thr_std_be = edca.groupby(['lambda'])['Throughput'].std()
    thr_n_be = edca.groupby(['lambda'])['Throughput'].count().iloc[1]
    thr_err_be = thr_std_be / math.sqrt(thr_n_be) * t.ppf(1 - alfa / 2, thr_n_be - 1)

    ns3_std_be = ns3_1.groupby(['lambda'])['thrpt'].std()
    ns3_n_be = ns3_1.groupby(['lambda'])['thrpt'].count().iloc[1]
    ns3_err_be = ns3_std_be / math.sqrt(ns3_n_be) * t.ppf(1 - alfa / 2, ns3_n_be - 1)

    ax1 = airtime_be.plot(marker='o', legend=True,yerr=thr_err_be,capsize=4)
    ax2 = ns3.plot(ax=ax1, marker='o', legend=True,yerr=ns3_err_be,capsize=4)

    ax2.legend(['Coex_wifi_v2','ns3'])
    ax2.set_xlabel('Per-station traffic intensity [packets/ms]', fontsize=14)
    ax2.set_ylabel('Aggregated throughput [Mb/s]', fontsize=14)

    plt.tight_layout()
    plt.savefig('results/LAMBDA/lambda_valid_v1.svg')

if __name__ == "__main__":
    #valid_airtime_data_v2()
    #valid_airtime_data()
    #valid_throughput_and_size()
    #valid_throughput()
    #valid_fair_index()
    #valid_thrpt_data_with_ns3_p2()
    valid_lambda_with_ns3()
    #valid_poisson_airtime_peak()
    #valid_poisson_airtime()
    #print_collision_prob()
    #print_airtime_34()
    #print_coexistance_airtime()
    #print_airtime_norm_per_station()
    #print_airtime_per_station()
    #print_channel_occupancy()
    #print_channel_efficency()

    #NRU RS
    #print_nru_airtime()
    #print_collision_prob_NRU()

    #NRU gap
    #print_collision_prob_NRU_gap()
    #print_nru_airtime_gap()

    #COEXY
    #print_coexistance_airtime()
    #print_coexistance_airtime_my()
    #print_coex()
    #print_matlab()
    #print_coex_gap_matlab()




