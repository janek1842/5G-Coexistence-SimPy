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
):

    backoffs = {key: {sum(stations_number.values()): 0} for key in range(cw_max + 1)}

    airtime_data = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}

    airtime_data_NR = {"Gnb {}".format(i): 0 for i in range(1, sum(gnb_number.values()) + 1)}
    airtime_control_NR = {"Gnb {}".format(i): 0 for i in range(1, sum(gnb_number.values()) + 1)}

    Queue = {"Station {}".format(i): [] for i in range(1, sum(stations_number.values()) + 1)}
    Queue.update({"Gnb {}".format(i): [] for i in range(1, sum(gnb_number.values()) + 1)})

    # random packet size generation (ERLANG DISTRIBUTION)
    #k = erlang.rvs(distribution_k,scale=1)
    k = 1
    payload_size = k * payload_size

    # 802.11ac Aggregation
    payload_size = nAMPDUs * payload_size

    run_simulation(stations_number, gnb_number, seeds, simulation_time,
                   Config(data_size=payload_size, cw_min=cw_min, cw_max=cw_max, r_limit=r_limit, mcs=mcs_value),
                   Config_NR(deter_period=16, observation_slot_duration=9, synchronization_slot_duration=sync,
                             max_sync_slot_desync=1000, min_sync_slot_desync=0, M=3, cw_min=cw_min, cw_max=cw_max,retry_limit=r_limit,mcot=6),
                   backoffs, airtime_data, airtime_control, airtime_data_NR, airtime_control_NR,poisson_lambda,transtime=transtime,
                   Queue=Queue,distribution_k=distribution_k,RTS_threshold=RTS_threshold,wifi_standard=wifi_standard,nMPDU=nAMPDUs,nSS=nSS,buffer_size=buffer_size)

if __name__ == "__main__":

    #Performing multiple runs
    list = []
    for radn in range(1,100):
        n = random.randint(10, 1000)
        list.append(n)

    print("SEEDS: ",list)

    # sync available values: 9, 18, 36, 63, 125, 250, 500, or 1000 [μs]

    for var in list:
        for i in [2,4,6,8,10,12,14,16,18,20,22]:

            # WiFi EDCA categories
            stationsConfig = {
                "backgroundStations": i,
                "bestEffortStations": i,
                "videoStations": i,
                "voiceStations": i
            }

            # NR-U categories
            gNBsConfig = {
                "class_1": i,
                "class_2": i,
                "class_3": i,
                "class_4": i
            }

            # for j in [1,10,20,30]:
            single_run(seeds=var,
                       stations_number=stationsConfig,
                       gnb_number=gNBsConfig,
                       simulation_time=10,
                       payload_size=1500,
                       cw_min=15,
                       cw_max=1023,
                       r_limit=7,
                       mcs_value=7,
                       poisson_lambda=2,
                       sync=9,
                       transtime=5000,
                       distribution_k = 1,
                       RTS_threshold = 9000000000,
                       wifi_standard = "802.11a", # 802.11ac or 802.11a
                       nAMPDUs = 1,
                       nSS = 1,
                       buffer_size = 3000000000
                       )