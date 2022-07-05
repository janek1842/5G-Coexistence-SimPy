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
        poisson_lambda
):

    backoffs = {key: {sum(stations_number.values()): 0} for key in range(cw_max + 1)}
    airtime_data = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    airtime_data_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}
    airtime_control_NR = {"Gnb {}".format(i): 0 for i in range(1, gnb_number + 1)}
    throughput_WiFI = {"Station {}".format(i): 0 for i in range(1, sum(stations_number.values()) + 1)}
    # run_simulation(stations_number, gnb_number, seeds, simulation_time, Config(payload_size, cw_min, cw_max, r_limit, mcs_value),
    #                backoffs, airtime_data, airtime_control)

    run_simulation(stations_number, gnb_number, seeds, simulation_time,
                   Config(payload_size, cw_min, cw_max, r_limit, mcs_value),
                   Config_NR(16, 9, 1000, 1000, 0, 3, cw_min, cw_max, 6),
                   backoffs, airtime_data, airtime_control, airtime_data_NR, airtime_control_NR,poisson_lambda)

if __name__ == "__main__":
    #  running diferent scenarios of simulation

    # performing single run
    # number = 2
    # single_run(seeds=7932
    #            , stations_number=1, gnb_number=0, simulation_time=10, payload_size=1472, cw_min=15, cw_max=1023, r_limit=7, mcs_value=7)

    #performing multiple runs
    list = []
    for radn in range(1, 3):
        n = random.randint(10, 1000)
        list.append(n)

    print("SEEDS: ",list)

    for var in list:
        for k in [1,2,5]:
            stationsConfig = {
                "backgroundStations": k,
                "bestEffortStations": k,
                "videoStations": k,
                "voiceStations": k
            }
        #for var in list:
        # k = 4
            single_run(seeds=var, stations_number=stationsConfig, gnb_number=0, simulation_time=10, payload_size=1500, cw_min=None,
                       cw_max=1023, r_limit=7, mcs_value=7,poisson_lambda=None)