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
        nAMPDUs
):

    backoffs = {key: {sum(stations_number.values()): 0} for key in range(cw_max + 1)}

    airtime_data = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}

    airtime_data_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}
    airtime_control_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}

    Queue = {"Station {}".format(i): [] for i in range(1, sum(stations_number.values()) + 1)}
    Queue.update({"Gnb {}".format(i): [] for i in range(1, gnb_number + 1)})

    # random packet size generation (ERLANG)
    #k = erlang.rvs(distribution_k,scale=1)
    k = 1

    # 802.11ac Aggregation
    payload_size = nAMPDUs * payload_size

    run_simulation(stations_number, gnb_number, seeds, simulation_time,
                   Config(data_size=k*payload_size, cw_min=cw_min, cw_max=cw_max, r_limit=r_limit, mcs=mcs_value),
                   Config_NR(deter_period=16, observation_slot_duration=9, synchronization_slot_duration=sync,
                             max_sync_slot_desync=1000, min_sync_slot_desync=0, M=3, cw_min=cw_min, cw_max=cw_max,retry_limit=r_limit,mcot=6),
                   backoffs, airtime_data, airtime_control, airtime_data_NR, airtime_control_NR,poisson_lambda,transtime=transtime,Queue=Queue,distribution_k=distribution_k,RTS_threshold=RTS_threshold,wifi_standard=wifi_standard,nMPDU=nAMPDUs)

if __name__ == "__main__":

    #performing multiple runs
    list = []
    for radn in range(1,10):
        n = random.randint(10, 1000)
        list.append(n)

    print("SEEDS: ",list)
    # 0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05
    # 0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.012,0.014
    for var in list:
        for k in [5,10,15,20,25,30,35]:

            stationsConfig = {
                "backgroundStations": 0,
                "bestEffortStations": 12,
                "videoStations": 0,
                "voiceStations": 0
            }

            single_run(seeds=var,
                       stations_number=stationsConfig,
                       gnb_number=0,
                       simulation_time=10,
                       payload_size=300,
                       cw_min=15,
                       cw_max=1023,
                       r_limit=7,
                       mcs_value=3,
                       poisson_lambda=None,
                       sync=0,
                       transtime=0,
                       distribution_k = 1,
                       RTS_threshold = 20000000000,
                       wifi_standard = "802.11ac", # 802.11ac or 802.11a
                       nAMPDUs = k
                       )

