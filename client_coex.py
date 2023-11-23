from coexistanceSimpy.Coexistence import *

def single_run(
        seeds: int,
        stations_number: int,
        gnb_number: int,
        simulation_time: int,
        cw_min: int or None,
        cw_max: int,
        r_limit: int,
        payload_size: int,
        mcs_value: int,
        poisson_lambda,
        sync,
        transtime,
        distribution_k,
        RTS_threshold,
        wifi_standard,
        nAMPDUs,
        nSS,
        buffer_size,
        buffer_controller,
        latency_entry_thresholds,
        latency_exit_thresholds
):

    backoffs = {key: {sum(stations_number.values()): 0} for key in range(cw_max + 1)}

    airtime_data = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    
    airtime_data_NR = {"Gnb {}".format(i): 0 for i in range(1, sum(gnb_number.values()) + 1)}
    airtime_control_NR = {"Gnb {}".format(i): 0 for i in range(1, sum(gnb_number.values()) + 1)}

    Queue = {"Station {}".format(i): [] for i in range(1, sum(stations_number.values()) + 1)}
    Queue.update({"Gnb {}".format(i): [] for i in range(1, sum(gnb_number.values()) + 1)})

    # Random packet size generation (Erlang Distribution)
    if distribution_k is not None:
        k = erlang.rvs(distribution_k,scale=1)
        payload_size = k * payload_size
    else:
        k = 1
        payload_size = k * payload_size

    # 802.11ac Aggregation
    payload_size = nAMPDUs * payload_size

    run_simulation(stations_number, gnb_number, seeds, simulation_time,
                   Config(data_size=payload_size, cw_min=cw_min, cw_max=cw_max, r_limit=r_limit, mcs=mcs_value),
                   Config_NR(deter_period=16, observation_slot_duration=9, synchronization_slot_duration=sync,
                             max_sync_slot_desync=1000, min_sync_slot_desync=0, M=3, cw_min=cw_min, cw_max=cw_max,retry_limit=r_limit,mcot=6),
                   backoffs, airtime_data, airtime_control, airtime_data_NR, airtime_control_NR,poisson_lambda,transtime=transtime,
                   Queue=Queue,distribution_k=distribution_k,RTS_threshold=RTS_threshold,wifi_standard=wifi_standard,nMPDU=nAMPDUs,nSS=nSS,buffer_size=buffer_size
                   ,buffer_controller=buffer_controller,latency_entry_thresholds=latency_entry_thresholds,latency_exit_thresholds=latency_exit_thresholds)

if __name__ == "__main__":

    #Performing multiple runs
    list = []
    for radn in range(1,101):
        n = random.randint(10, 1000)
        list.append(n)

    print("SEEDS: ",list)

    # sync slot available values: 9, 18, 36, 63, 125, 250, 500, or 1000 [μs]

    for var in list:
        for i in [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]:

            # WiFi EDCA categories - configuration of stations participating in simulation
            stationsConfig = {
                "backgroundStations": 1,
                "bestEffortStations": 0,
                "videoStations": 1,
                "voiceStations": 0
            }

            # NR-U categories - configuration of gNodeBs participating in simulation
            gNBsConfig = {
                "class_4": 1,
                "class_3": 0,
                "class_2": 1,
                "class_1": 0
            }

            # Latency thresholds defined per Wi-Fi/NR-U Access Category. This value is validated if any packet's latency in Queue exceeds this value
            latency_entry_thresholds = {
                "be": 10000000000000,
                "bk": 10000000000000,
                "vi": 10000000000000,
                "vo": 10000000000000,
                "c1": 10000000000000,
                "c2": 10000000000000,
                "c3": 10000000000000,
                "c4": 10000000000000,
            }

            # Latency thresholds defined per Wi-Fi/NR-U Access Category. This value is validated if packet to be transmitted is already delayed over this threshold
            latency_exit_thresholds = {
                "be": 1,
                "bk": 1,
                "vi": 1,
                "vo": 1,
                "c1": 1,
                "c2": 1,
                "c3": 1,
                "c4": 1,
            }

            # for j in [1,10,20,30]:
            single_run(seeds=var,
                       stations_number=stationsConfig,
                       gnb_number=gNBsConfig,
                       simulation_time=100,
                       payload_size=1500,
                       cw_min=15,
                       cw_max=1023,
                       r_limit=4,
                       mcs_value=7,
                       poisson_lambda=i,
                       sync=250,
                       transtime=5600,
                       distribution_k = None,
                       RTS_threshold = 9000000000,
                       wifi_standard = "802.11a", # 802.11ac or 802.11a
                       nAMPDUs = 1,
                       nSS = 1,
                       buffer_size = 1000,
                       buffer_controller=1,
                       latency_entry_thresholds = latency_entry_thresholds,
                       latency_exit_thresholds = latency_exit_thresholds
                       )
