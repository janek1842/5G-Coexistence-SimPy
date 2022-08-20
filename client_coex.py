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
        transtime
):

    backoffs = {key: {sum(stations_number.values()): 0} for key in range(cw_max + 1)}

    airtime_data = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}

    airtime_data_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}
    airtime_control_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}

    run_simulation(stations_number, gnb_number, seeds, simulation_time,
                   Config(payload_size, cw_min, cw_max, r_limit, mcs_value),
                   Config_NR(deter_period=16, observation_slot_duration=9, synchronization_slot_duration=sync,
                             max_sync_slot_desync=1000, min_sync_slot_desync=0, M=3, cw_min=cw_min, cw_max=cw_max,retry_limit=r_limit),
                   backoffs, airtime_data, airtime_control, airtime_data_NR, airtime_control_NR,poisson_lambda,transtime=transtime)

if __name__ == "__main__":

    #performing multiple runs
    list = []
    for radn in range(1,11):
        n = random.randint(10, 1000)
        list.append(n)

    print("SEEDS: ",list)

    for var in list:
        for k in [9,18,36,63,125,250,500,1000]:

            stationsConfig = {
                "backgroundStations": 0,
                "bestEffortStations": 12,
                "videoStations": 0,
                "voiceStations": 0
            }

            single_run(seeds=var,
                       stations_number=stationsConfig,
                       gnb_number=12,
                       simulation_time=100,
                       payload_size=1500,
                       cw_min=512,
                       cw_max=1023,
                       r_limit=7,
                       mcs_value=7,
                       poisson_lambda=None,
                       sync=k,
                       transtime=5400
                       )

