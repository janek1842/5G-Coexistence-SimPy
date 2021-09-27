import logging
import threading
from typing import Dict, List, Optional, Tuple

from coexistanceSimpy.Coexistence import *


def single_run(
        seeds: int,
        stations_number: int,
        simulation_time: int,
        cw_min: int,
        cw_max: int,
        r_limit: int,
        payload_size: int,
        mcs_value: int,
):
    backoffs = {key: {stations_number: 0} for key in range(cw_max + 1)}
    airtime_data = {"Station {}".format(i): 0 for i in range(1, stations_number + 1)}
    airtime_control = {"Station {}".format(i): 0 for i in range(1, stations_number + 1)}
    run_simulation(stations_number, seeds, simulation_time, Config(payload_size, cw_min, cw_max, r_limit, mcs_value),
                   backoffs, airtime_data, airtime_control)


def run_changing_stations(
        runs: int,
        seed: int,
        stations_start: int,
        stations_end: int,
        simulation_time: int,
        cw_min: int,
        cw_max: int,
        r_limit: int,
        payload_size: int,
        mcs_value: int,
):
    config = Config(payload_size, cw_min, cw_max, r_limit, mcs_value)
    backoffs = {
        key: {i: 0 for i in range(stations_start, stations_end + 1)}
        for key in range(cw_max + 1)
    }

    airtime_data = {num_stations: {"Station {}".format(i): 0 for i in range(1, num_stations + 1)} for num_stations in range(stations_start, stations_end + 1)}
    airtime_control = {num_stations: {"Station {}".format(i): 0 for i in range(1, num_stations + 1)} for num_stations in range(stations_start, stations_end + 1)}


    for _ in range(runs):
        threads = [
            threading.Thread(
                target=run_simulation,
                args=(
                    n,
                    seed * _,
                    simulation_time,
                    config,
                    backoffs,
                    airtime_data[n],
                    airtime_control[n],
                ),
            )
            for n in range(stations_start, stations_end + 1)
        ]
        __start_threads(threads)


def __start_threads(threads: List[threading.Thread]):
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    #  running diferent scenarios of simulation

    run_changing_stations(runs=5, seed=128, stations_start=10, stations_end=10, simulation_time=100, payload_size=1472, cw_min=15, cw_max=1023, r_limit=7, mcs_value=7)

    #single_run(seeds=123, stations_number=10, simulation_time=10, payload_size=1472, cw_min=15, cw_max=1023, r_limit=7, mcs_value=7)