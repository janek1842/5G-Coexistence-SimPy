import logging
import csv
import os
import random
import time
import pandas as pd
import simpy
import numpy
import threading
import string
from numpy.random import RandomState
from dataclasses import dataclass, field
from typing import Dict, List
from scipy.stats import erlang,pareto,exponnorm,lognorm,triang
#from numpy.random import pareto
from .Times import *
from datetime import datetime
from collections import defaultdict

output_csv = "csvresults/V4/latency/test7.csv"
file_log_name = f"{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.log"

typ_filename = "RS_coex_1sta_1wifi2.log"

RTS_global_flag = True
RTS_transmitter = ""

logging.basicConfig(filename="",format='%(asctime)s %(message)s',filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)  # chose DEBUG to display stats in debug mode

colors = [
    "\033[30m",
    "\033[32m",
    "\033[31m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
    "\033[36m",
    "\033[37m",
]  # colors to distinguish stations in output

big_num = 1000000  # some big number for quesing in peeemtive resources - big starting point

gap = True

class Channel_occupied(Exception):
    pass

@dataclass()
class Config:
    data_size: int = 1472 # size od payload in b
    cw_min: int = 15  # min cw window size
    cw_max: int = 1023  # max cw window size 1023 def
    r_limit: int = 7
    mcs: int = 7
    aifsn: int = 3
    RTS_threshold: int = 3000
    standard: string = "802.11a"
    nAMPDU: int = 1
    nSS: int = 1

@dataclass()
class Config_NR:
    cw_min: int
    synchronization_slot_duration: int = 1000
    deter_period: int = 16  # time used for waiting in prioritization period, microsec
    observation_slot_duration: int = 9  # observation slot in mikros
    max_sync_slot_desync: int = 1000
    min_sync_slot_desync: int = 0

    # channel access class related:
    M: int = 3  # amount of observation slots to wait after deter perion in prioritization period
    cw_max: int = 1023
    mcot: int = 6  # max ocupancy time
    retry_limit: int = 7

def random_sample(max, number, min_distance=0):  # func used to desync gNBs
    # returns number * elements <0, max>
    samples = random.sample(range(max - (number - 1) * (min_distance - 1)), number)
    indices = sorted(range(len(samples)), key=lambda i: samples[i])
    ranks = sorted(indices, key=lambda i: indices[i])
    return [sample + (min_distance - 1) * rank for sample, rank in zip(samples, ranks)]

def log(gnb, mes: str) -> None:
    logger.info(
        f"{gnb.col}Time: {gnb.env.now} Station: {gnb.name} Message: {mes}"
    )

class Station:
    def __init__(
            self,
            env: simpy.Environment,
            name: str,
            channel: dataclass,
            transtime: int,
            config: Config = Config(),
            simulation_time: int = 10,
            poisson_lambda: int = 10,
            backoffs: dict = {},
            Queue: dict = {},
            buffer_size: int = 10
    ):
        self.backoffs = backoffs
        self.transtime = transtime
        self.config = config
        self.times = Times(config.data_size, config.mcs,config.aifsn,config.standard,self.config.nSS)  # using Times script to get time calculations
        self.name = name  # name of the station
        self.env = env  # simpy environment
        self.col = random.choice(colors)  # color of output -- for future station distinction
        self.frame_to_send = None  # the frame object which is next to send
        self.succeeded_transmissions = 0  # all succeeded transmissions for station
        self.failed_transmissions = 0  # all failed transmissions for station
        self.failed_transmissions_in_row = 0  # all failed transmissions for station in a row
        self.cw_min = self.config.cw_min  # cw min parameter value
        self.cw_max = self.config.cw_max  # cw max parameter value
        self.channel = channel  # channel obj
        self.simulation_time = simulation_time
        self.main_process = env.process(self.start())  # starting simulation process
        self.process = None  # waiting back off process
        self.channel.airtime_data.update({name: 0})
        self.channel.airtime_control.update({name: 0})
        self.first_interrupt = False
        self.back_off_time = 0
        self.start = 0
        self.sumTime = 0
        self.poisson_lambda = poisson_lambda
        self.sumTime =0
        self.simulation_time = simulation_time
        self.Queue = Queue
        self.buffer_size = buffer_size

    def wait_for_frame(self,time_to_wait):
        yield self.env.timeout(time_to_wait)
        self.start_generating()

    def start_generating(self):
        self.sumTime = numpy.random.exponential(1 / self.poisson_lambda) * 1000
        if self.buffer_size is None or len(self.Queue[self.name]) <= self.buffer_size:
            self.Queue[self.name].append(self.generate_new_frame())
            #self.frame_to_send = self.generate_new_frame()

        self.env.process(self.wait_for_frame(self.sumTime))

    def start(self):
        if self.poisson_lambda is not None:
            self.start_generating()
        global RTS_global_flag

        while True:
            if len(self.Queue[self.name]) > 0 or self.poisson_lambda is None:
                if self.poisson_lambda is not None:
                    self.frame_to_send = self.Queue[self.name][0]
                    self.Queue[self.name].pop(0)
                    self.was_sent = False
                    pass

                while not self.was_sent:
                    if self.frame_to_send is not None:
                            self.process = self.env.process(self.wait_back_off())
                            yield self.process

                            if RTS_global_flag and self.config.data_size >= self.config.RTS_threshold:
                                RTS_global_flag = False
                                yield self.env.timeout(self.times.get_rts_cts_time())
                                self.was_sent = yield self.env.process(self.send_frame())
                                RTS_global_flag = True

                            elif self.config.data_size < self.config.RTS_threshold:
                                self.was_sent = yield self.env.process(self.send_frame())

                    else:
                        self.was_sent = True

            elif bool([a for a in self.Queue.values() if a == []]):
                yield self.env.timeout(1000)
            else:
                #yield self.env.timeout(1000)
                self.env.step()

    def wait_back_off(self):

        self.back_off_time = self.generate_new_back_off_time(
            self.failed_transmissions_in_row)  # generating the new Back Off time

        while self.back_off_time > -1:
            try:
                with self.channel.tx_lock.request() as req:  # waiting  for idle channel -- empty channel
                    yield req

                self.back_off_time += self.times.t_difs  # add DIFS time

                log(self, f"Starting to wait backoff (with DIFS): ({self.back_off_time})u...")
                self.first_interrupt = True
                self.start = self.env.now  # store the current simulation time
                self.channel.back_off_list.append(self)  # join the list off stations which are waiting Back Offs


                yield self.env.timeout(self.back_off_time)  # join the environment action queue


                log(self, f"Backoff waited, sending frame...")

                self.back_off_time = -1  # leave the loop
                self.channel.back_off_list.remove(self)  # leave the waiting list as Backoff was waited successfully


            except simpy.Interrupt:  # handle the interruptions from transmitting stations
                if self.first_interrupt and self.start is not None:
                    #tak jest po mojemu:
                    log(self, "Waiting was interrupted, waiting to resume backoff...")
                    all_waited = self.env.now - self.start
                    if all_waited <= self.times.t_difs:
                        self.back_off_time -= self.times.t_difs
                        log(self, f"Interupted in DIFS ({self.times.t_difs}), backoff {self.back_off_time}")
                    else:
                        back_waited = all_waited - self.times.t_difs
                        slot_waited = int(back_waited / self.times.t_slot)
                        self.back_off_time -= ((slot_waited * self.times.t_slot) + self.times.t_difs)
                        log(self,
                            f"Completed slots(9us) {slot_waited} = {(slot_waited * self.times.t_slot)}  plus DIFS time {self.times.t_difs}")
                        log(self,
                            f"Backoff decresed by {((slot_waited * self.times.t_slot) + self.times.t_difs)} new Backoff {self.back_off_time}")
                    self.first_interrupt = False

    def send_frame(self):

        self.channel.tx_list.append(self)  # add station to currently transmitting list

        res = self.channel.tx_queue.request(
            priority=(big_num - self.frame_to_send.frame_time))  # create request basing on this station frame length

        try:
            result = yield res | self.env.timeout(0)  # try to hold transmitting lock(station with the longest frame will get this)

            if res not in result:  # check if this station got lock, if not just wait you frame time
                raise simpy.Interrupt("There is a longer frame...")

            with self.channel.tx_lock.request() as lock:  # this station has the longest frame so hold the lock
                yield lock

                for station in self.channel.back_off_list:  # stop all station which are waiting backoff as channel is not idle
                    if station.process.is_alive:
                        station.process.interrupt()
                for gnb in self.channel.back_off_list_NR:  # stop all station which are waiting backoff as channel is not idle
                    if gnb.process.is_alive:
                        gnb.process.interrupt()

                log(self, f'Starting sending frame: {self.frame_to_send.frame_time}')

                yield self.env.timeout(self.frame_to_send.frame_time)  # wait this station frame time

                self.channel.back_off_list.clear()  # channel idle, clear backoff waiting list
                was_sent = self.check_collision()  # check if collision occurred

                if was_sent:  # transmission successful
                    self.channel.airtime_control[self.name] += self.times.get_ack_frame_time() + self.times.t_difs
                    yield self.env.timeout(self.times.get_ack_frame_time())  # wait ack
                    self.channel.tx_list.clear()  # clear transmitting list
                    self.channel.tx_list_NR.clear()
                    self.channel.tx_queue.release(res)  # leave the transmitting queue

                    return True

                # there was collision
                self.channel.tx_list.clear()  # clear transmitting list
                self.channel.tx_list_NR.clear()
                self.channel.tx_queue.release(res)  # leave the transmitting queue
                self.channel.tx_queue = simpy.PreemptiveResource(self.env,
                                                                 capacity=1)  # create new empty transmitting queue
                self.channel.airtime_control[self.name] += self.times.ack_timeout
                yield self.env.timeout(self.times.ack_timeout)  # simulate ack timeout after failed transmission
                return False

        except simpy.Interrupt:  # this station does not have the longest frame, waiting frame time
             # self.channel.airtime_control[self.name] += self.frame_to_send.frame_time
             yield self.env.timeout(self.frame_to_send.frame_time)

        was_sent = self.check_collision()

        if was_sent:  # check if collision occurred
            log(self, f'Waiting for ACK time: {self.times.get_ack_frame_time()}')
            self.channel.airtime_control[self.name] += self.times.get_ack_frame_time()
            yield self.env.timeout(self.times.get_ack_frame_time())  # wait ack
        else:
            log(self, "waiting ack timeout slave")
            self.channel.airtime_control[self.name] += Times.ack_timeout
            yield self.env.timeout(Times.ack_timeout)  # simulate ack timeout after failed transmission
        return was_sent

    def check_collision(self):  # check if the collision occurred
        if (len(self.channel.tx_list) + len(self.channel.tx_list_NR)) > 1 or (len(self.channel.tx_list) + len(self.channel.tx_list_NR)) == 0 :
            self.sent_failed()
            return False
        else:
            self.sent_completed()
            return True

    def generate_new_back_off_time(self, failed_transmissions_in_row):

        upper_limit = (pow(2, failed_transmissions_in_row) * (
                self.config.cw_min + 1) - 1)  # define the upper limit basing on  unsuccessful transmissions in the row
        upper_limit = (
            upper_limit if upper_limit <= self.cw_max else self.cw_max)  # set upper limit to CW Max if is bigger then this parameter
        back_off = random.randint(0, upper_limit)  # draw the back off value
        self.backoffs[back_off][1] += 1  # store drawn value for future analyzess
        return back_off * self.times.t_slot

    def generate_new_frame(self):
        #frame_length = self.times.get_ppdu_frame_time(self.config.nAMPDU)
        frame_length = self.transtime
        return Frame(frame_length, self.name, self.col, self.config.data_size, self.env.now)

    def sent_failed(self):
        log(self, "There was a collision")
        self.frame_to_send.number_of_retransmissions += 1
        self.channel.failed_transmissions += 1
        self.failed_transmissions += 1
        self.failed_transmissions_in_row += 1

        log(self, self.channel.failed_transmissions)

        if self.frame_to_send.number_of_retransmissions > self.config.r_limit:
            self.frame_to_send = self.generate_new_frame()
            self.failed_transmissions_in_row = 0

    def getTypeFromStation(self):
        if self.config.cw_min == 15 and self.config.cw_max == 1023 and self.config.aifsn == 7:
            return "bg"
        elif self.config.cw_min == 15 and self.config.cw_max == 1023 and self.config.aifsn == 3:
            return "be"
        elif self.config.cw_min == 7 and self.config.cw_max == 15 and self.config.aifsn == 2:
            return "vd"
        elif self.config.cw_min == 3 and self.config.cw_max == 7 and self.config.aifsn == 2:
            return "vo"

    def packet_dropped(self):
        log(self, "Frame dropped")
        self.channel.failed_transmissions += 1
        self.failed_transmissions += 1
        self.failed_transmissions_in_row += 1
        log(self, self.channel.failed_transmissions)

        if self.frame_to_send.number_of_retransmissions > self.config.r_limit:
            self.frame_to_send = self.generate_new_frame()
            self.failed_transmissions_in_row = 0

    def sent_completed(self):
        log(self, f"Successfully sent frame, waiting ack: {self.times.get_ack_frame_time()}")
        self.frame_to_send.t_end = self.env.now
        self.frame_to_send.t_to_send = (self.frame_to_send.t_end - self.frame_to_send.t_start)

        self.channel.latency_wifi.append(self.frame_to_send.t_to_send)

        self.channel.succeeded_transmissions += 1

        if self.config.cw_min == 15 and self.config.cw_max == 1023 and self.config.aifsn==7:
            self.channel.succeeded_transmissions_bg += 1
            self.channel.latency_bg.append(self.frame_to_send.t_to_send)
        elif self.config.cw_min == 15 and self.config.cw_max == 1023 and self.config.aifsn == 3:
            self.channel.succeeded_transmissions_be += 1
            self.channel.latency_be.append(self.frame_to_send.t_to_send)
        elif self.config.cw_min == 3 and self.config.cw_max == 15 and self.config.aifsn == 2:
            self.channel.succeeded_transmissions_vd += 1
            self.channel.latency_vd.append(self.frame_to_send.t_to_send)
        else:
            self.channel.succeeded_transmissions_vc += 1
            self.channel.latency_vc.append(self.frame_to_send.t_to_send)

        self.succeeded_transmissions += 1
        self.failed_transmissions_in_row = 0
        self.channel.bytes_sent += self.frame_to_send.data_size
        self.channel.airtime_data[self.name] += self.frame_to_send.frame_time

        return True

class Gnb:
    def __init__(
            self,
            env: simpy.Environment,
            name: str,
            channel: dataclass,
            config_nr,
            transtime,
            backoffs,
            poisson_lambda,
            Queue,
            buffer_size
    ):
        self.config_nr = config_nr
        self.buffer_size = buffer_size
        self.transtime = transtime
        # self.times = Times(config.data_size, config.mcs)  # using Times script to get time calculations
        self.name = name  # name of the station
        self.env = env  # simpy environment
        self.col = random.choice(colors)  # color of output -- for future station distinction
        self.transmission_to_send = None  # the transmision object which is next to send
        self.succeeded_transmissions = 0  # all succeeded transmissions for station
        self.failed_transmissions = 0  # all failed transmissions for station
        self.failed_transmissions_in_row = 0  # all failed transmissions for station in a row

        self.cw_min = config_nr.cw_min  # cw min parameter value
        self.N = None  # backoff counter
        self.desync = 0
        self.next_sync_slot_boundry = 0

        self.cw_max = config_nr.cw_max  # cw max parameter value
        self.channel = channel  # channel objfirst_transmission
        env.process(self.start())  # starting simulation process
        env.process(self.sync_slot_counter())
        self.process = None  # waiting back off process
        self.channel.airtime_data_NR.update({name: 0})
        self.channel.airtime_control_NR.update({name: 0})
        self.desync_done = False
        self.first_interrupt = False
        self.back_off_time = 0
        self.time_to_next_sync_slot = 0
        self.waiting_backoff = False
        self.start_nr = 0
        self.backoffs = backoffs
        self.poisson_lambda = poisson_lambda
        self.Queue = Queue


    def wait_for_frame(self,time_to_wait):
        yield self.env.timeout(time_to_wait)
        self.start_generating()

    def start_generating(self):
        self.sumTime = numpy.random.exponential(1 / self.poisson_lambda) * 1000
        if self.buffer_size is None or len(self.Queue[self.name]) <= self.buffer_size:
            self.Queue[self.name].append(self.gen_new_transmission())
            #self.transmission_to_send=self.gen_new_transmission()
        self.env.process(self.wait_for_frame(self.sumTime))

    def start(self):
        if self.poisson_lambda is not None:
            self.start_generating()

        while True:
            if len(self.Queue[self.name]) > 0 or self.poisson_lambda is None:
                if self.poisson_lambda is not None:
                    self.transmission_to_send = self.Queue[self.name][0]
                    self.Queue[self.name].pop(0)
                    self.was_sent = False
                    pass
                else:
                    pass

                while not self.was_sent:
                    if gap:
                        self.process = self.env.process(self.wait_back_off_gap())
                        yield self.process
                        self.was_sent = yield self.env.process(self.send_transmission())
                    else:
                        self.process = self.env.process(self.wait_back_off())
                        yield self.process
                        self.was_sent = yield self.env.process(self.send_transmission())
            elif bool([a for a in self.Queue.values() if a == []]):
                self.env.step()

    def wait_back_off_gap(self):
        self.back_off_time = self.generate_new_back_off_time(self.failed_transmissions_in_row)
        m = self.config_nr.M
        prioritization_period_time = self.config_nr.deter_period + m * self.config_nr.observation_slot_duration

        self.back_off_time += prioritization_period_time  # add Priritization Period time to bacoff procedure

        while self.back_off_time > -1:
            try:
                with self.channel.tx_lock.request() as req:  # waiting  for idle channel -- empty channel
                    yield req

                self.time_to_next_sync_slot = self.next_sync_slot_boundry - self.env.now

                log(self, f'Backoff = {self.back_off_time} , and time to next slot: {self.time_to_next_sync_slot}')
                while self.back_off_time >= self.time_to_next_sync_slot:
                    self.time_to_next_sync_slot += self.config_nr.synchronization_slot_duration
                    log(self,f'Backoff > time to sync slot: new time to next possible sync +1000 = {self.time_to_next_sync_slot}')

                gap_time = self.time_to_next_sync_slot - self.back_off_time
                log(self, f"Waiting gap period of : {gap_time} us")
                assert gap_time >= 0, "Gap period is < 0!!!"

                yield self.env.timeout(gap_time)
                log(self, f"Finished gap period")

                self.first_interrupt = True
                self.start_nr = self.env.now  # store the current simulation time

                log(self, f'Channels in use by {self.channel.tx_lock.count} stations')

                # checking if channel if idle
                if (len(self.channel.tx_list_NR) + len(self.channel.tx_list)) > 0:
                    # if self.channel.tx_lock.count > 0:
                    log(self, 'Channel busy -- waiting to be free')
                    with self.channel.tx_lock.request() as req:
                        yield req
                    log(self, 'Finished waiting for free channel - restarting backoff procedure')

                else:
                    log(self, 'Channel free')

                    log(self, f"Starting to wait backoff: ({self.back_off_time}) us...")
                    self.channel.back_off_list_NR.append(self)  # join the list off stations which are waiting Back Offs
                    self.waiting_backoff = True

                    yield self.env.timeout(self.back_off_time)  # join the environment action queue

                    log(self, f"Backoff waited, sending frame...")
                    self.back_off_time = -1  # leave the loop
                    self.waiting_backoff = False
                    self.first_interrupt = False

                    self.channel.back_off_list_NR.remove(
                        self)  # leave the waiting list as Backoff was waited successfully


            except simpy.Interrupt:  # handle the interruptions from transmitting stations
                log(self, "Waiting was interrupted")

                if self.first_interrupt and self.start is not None and self.waiting_backoff is True:
                    log(self, "Backoff was interrupted, waiting to resume backoff...")
                    already_waited = self.env.now - self.start_nr

                    if already_waited <= prioritization_period_time:
                        self.back_off_time -= prioritization_period_time
                        log(self, f"Interrupted in PP time {prioritization_period_time}, backoff {self.back_off_time}")
                    else:
                        slots_waited = int((already_waited - prioritization_period_time) / self.config_nr.observation_slot_duration)
                        self.back_off_time -= ((slots_waited * self.config_nr.observation_slot_duration) + prioritization_period_time)
                        log(self, f"Completed slots(9us) {slots_waited} = {(slots_waited * self.config_nr.observation_slot_duration)}  plus PP time {prioritization_period_time}")
                        log(self, f"Backoff decresed by {(slots_waited * self.config_nr.observation_slot_duration) + prioritization_period_time} new Backoff {self.back_off_time}")

                    self.back_off_time += prioritization_period_time  # addnin new PP before next weiting
                    self.first_interrupt = False
                    self.waiting_backoff = False

    def wait_back_off(self):
        global start
        self.back_off_time = self.generate_new_back_off_time(failed_transmissions_in_row=self.failed_transmissions_in_row)
        m = self.config_nr.M

        prioritization_period_time = self.config_nr.deter_period + m * self.config_nr.observation_slot_duration
        self.back_off_time += prioritization_period_time  # add Priritization Period time to bacoff procedure

        while self.back_off_time > -1:
            # m = self.config_nr.M
            # prioritization_period_time = self.config_nr.deter_period + m * self.config_nr.observation_slot_duration

            try:
                with self.channel.tx_lock.request() as req:  # waiting  for idle channel -- empty channel
                    yield req

                self.first_interrupt = True
                self.back_off_time += prioritization_period_time  # add Priritization Period time to bacoff procedure
                log(self, f"Starting to wait backoff (with PP): ({self.back_off_time}) us...")
                start = self.env.now  # store the current simulation time
                self.channel.back_off_list_NR.append(self)  # join the list off stations which are waiting Back Offs

                yield self.env.timeout(self.back_off_time)  # join the environment action queue

                log(self, f"Backoff waited, sending frame...")
                self.back_off_time = -1  # leave the loop

                self.channel.back_off_list_NR.remove(self)  # leave the waiting list as Backoff was waited successfully

            except simpy.Interrupt:  # handle the interruptions from transmitting stations
                log(self, "Backoff was interrupted, waiting to resume backoff...")
                if self.first_interrupt and start is not None:
                    already_waited = self.env.now - start

                    if already_waited <= prioritization_period_time:
                        self.back_off_time -= prioritization_period_time
                        log(self, f"Interrupted in PP time {prioritization_period_time}, backoff {self.back_off_time}")
                    else:
                        slots_waited = int((already_waited - prioritization_period_time) / self.config_nr.observation_slot_duration)
                        # self.back_off_time -= already_waited  # set the Back Off to the remaining one
                        self.back_off_time -= ((slots_waited * self.config_nr.observation_slot_duration) + prioritization_period_time)
                        log(self, f"Completed slots(9us) {slots_waited} = {(slots_waited * self.config_nr.observation_slot_duration)}  plus PP time {prioritization_period_time}")
                        log(self, f"Backoff decresed by {(slots_waited * self.config_nr.observation_slot_duration) + prioritization_period_time} new Backoff {self.back_off_time}")

                    self.first_interrupt = False
                    self.waiting_backoff = False

    def sync_slot_counter(self):
        # Process responsible for keeping the next sync slot boundry timestamp
        self.desync = random.randint(self.config_nr.min_sync_slot_desync, self.config_nr.max_sync_slot_desync)
        self.next_sync_slot_boundry = self.desync
        log(self, f"Selected random desync to {self.desync} us")
        yield self.env.timeout(self.desync)  # randomly desync tx starting points
        while True:
            self.next_sync_slot_boundry += self.config_nr.synchronization_slot_duration
            log(self, f"Next synch slot boundry is: {self.next_sync_slot_boundry}")
            yield self.env.timeout(self.config_nr.synchronization_slot_duration)

    def send_transmission(self):
        self.channel.tx_list_NR.append(self)  # add station to currently transmitting list
        #self.transmission_to_send = self.gen_new_transmission()
        res = self.channel.tx_queue.request(priority=(
                big_num - self.transmission_to_send.transmission_time))  # create request basing on this station frame length

        try:
            result = yield res | self.env.timeout(
                0)  # try to hold transmitting lock(station with the longest frame will get this)

            if res not in result:  # check if this station got lock, if not just wait you frame time

                raise simpy.Interrupt("There is a longer frame...")
                # self.env.timeout(self.transmission_to_send.transmission_time)
                # return False

            with self.channel.tx_lock.request() as lock:  # this station has the longest frame so hold the lock
                yield lock
                # log(self, f'{self.channel.back_off_list_NR}')

                for station in self.channel.back_off_list:  # stop all station which are waiting backoff as channel is not idle
                    # if station.process is not None:
                    #     station.process.interrupt()
                    if station.process.is_alive:
                        station.process.interrupt()
                for gnb in self.channel.back_off_list_NR:  # stop all station which are waiting backoff as channel is not idle
                    # if gnb.process is not None:
                    #     gnb.process.interrupt()
                    if gnb.process.is_alive:
                        gnb.process.interrupt()

                log(self, f'Transmission will be for: {self.transmission_to_send.transmission_time} time')

                yield self.env.timeout(self.transmission_to_send.transmission_time )

                self.channel.back_off_list_NR.clear()  # channel idle, clear backoff waiting list
                was_sent = self.check_collision()  # check if collision occurred

                if was_sent:  # transmission successful
                    self.channel.airtime_control_NR[self.name] += self.transmission_to_send.rs_time
                    log(self, f"adding rs time to control data: {self.transmission_to_send.rs_time}")
                    self.channel.airtime_data_NR[self.name] += self.transmission_to_send.airtime
                    log(self, f"adding data airtime to data: {self.transmission_to_send.airtime}")
                    self.channel.tx_list_NR.clear()  # clear transmitting list
                    self.channel.tx_list.clear()
                    self.channel.tx_queue.release(res)  # leave the transmitting queue
                    return True

            # there was collision
            self.channel.tx_list_NR.clear()  # clear transmitting list
            self.channel.tx_list.clear()
            self.channel.tx_queue.release(res)  # leave the transmitting queue
            self.channel.tx_queue = simpy.PreemptiveResource(self.env,capacity=1)  # create new empty transmitting queue
            return False

        except simpy.Interrupt:  # this station does not have the longest frame, waiting frame time
            yield self.env.timeout(self.transmission_to_send.transmission_time)


        was_sent = self.check_collision()
        return was_sent

    def check_collision(self):  # check if the collision occurred
        if gap:
            if (len(self.channel.tx_list) + len(self.channel.tx_list_NR)) > 1 or (len(self.channel.tx_list) + len(self.channel.tx_list_NR)) == 0:
                self.sent_failed()
                return False
            else:
                self.sent_completed()
                return True
        else:
            if (len(self.channel.tx_list) + len(self.channel.tx_list_NR)) > 1 or (len(self.channel.tx_list) + len(self.channel.tx_list_NR)) == 0:
                self.sent_failed()
                return False
            else:
                self.sent_completed()
                return True

    def gen_new_transmission(self):

        #transmission_time = self.config_nr.mcot * 1000  # transforming to usec
        transmission_time = self.transtime
        if gap:
            rs_time = 0
        else:
            rs_time = self.next_sync_slot_boundry - self.env.now
        airtime = transmission_time - rs_time

        return Transmission_NR(transmission_time, self.name, self.col, self.env.now, airtime, rs_time)

    def generate_new_back_off_time(self, failed_transmissions_in_row):
        # BACKOFF TIME GENERATION

        upper_limit = (pow(2,failed_transmissions_in_row) * (
                self.config_nr.cw_min + 1) - 1)  # define the upper limit basing on  unsuccessful transmissions in the row
        upper_limit = (
            upper_limit if upper_limit <= self.cw_max else self.cw_max)  # set upper limit to CW Max if is bigger then this parameter
        back_off = random.randint(0, upper_limit)  # draw the back off value
        #print(self)
        self.backoffs[back_off][1] += 1  # store drawn value for future analyzes
        return back_off * self.config_nr.observation_slot_duration

    def sent_failed(self):
        log(self, "There was a collision")

        self.transmission_to_send.number_of_retransmissions += 1
        self.channel.failed_transmissions_NR += 1
        self.failed_transmissions += 1
        self.failed_transmissions_in_row += 1
        log(self, self.channel.failed_transmissions_NR)

        if self.transmission_to_send.number_of_retransmissions > self.config_nr.retry_limit:
            self.transmission_to_send=self.gen_new_transmission()
            self.failed_transmissions_in_row = 0

    def getTypeFromgNb(self):
        if self.config_nr.cw_min == 15 and self.config_nr.cw_max == 1023 and self.config_nr.M == 7:
            return "c4"
        elif self.config_nr.cw_min == 15 and self.config_nr.cw_max == 63 and self.config_nr.M == 3:
            return "c3"
        elif self.config_nr.cw_min == 7 and self.config_nr.cw_max == 15 and self.config_nr.M == 1:
            return "c2"
        elif self.config_nr.cw_min == 3 and self.config_nr.cw_max == 7 and self.config_nr.M == 1:
            return "c1"

    def sent_completed(self):
        log(self, f"Successfully sent transmission")
        self.transmission_to_send.t_end = self.env.now
        self.transmission_to_send.t_to_send = (self.transmission_to_send.t_end - self.transmission_to_send.t_start)
        self.channel.latency_nru.append(self.transmission_to_send.t_to_send)

        self.channel.succeeded_transmissions_NR += 1
        self.succeeded_transmissions += 1
        self.failed_transmissions_in_row = 0

        if self.config_nr.cw_min == 15 and self.config_nr.cw_max == 1023 and self.config_nr.M==7:
            self.channel.succeeded_transmissions_c4 += 1
            self.channel.latency_c4.append(self.transmission_to_send.t_to_send)

        elif self.config_nr.cw_min == 15 and self.config_nr.cw_max == 63 and self.config_nr.M==3:
            self.channel.succeeded_transmissions_c3 += 1
            self.channel.latency_c3.append(self.transmission_to_send.t_to_send)

        elif self.config_nr.cw_min == 7 and self.config_nr.cw_max == 15 and self.config_nr.M==1:
            self.channel.succeeded_transmissions_c2 += 1
            self.channel.latency_c2.append(self.transmission_to_send.t_to_send)

        elif self.config_nr.cw_min == 3 and self.config_nr.cw_max == 7 and self.config_nr.M == 1:
            self.channel.succeeded_transmissions_c1 += 1
            self.channel.latency_c1.append(self.transmission_to_send.t_to_send)

        return True

@dataclass()
class Channel:
    tx_queue: simpy.PreemptiveResource  # lock for the stations with the longest frame to transmit
    tx_lock: simpy.Resource  # channel lock (locked when there is ongoing transmission)
    rts_lock: simpy.Resource # RTS / CTS lock (the transmitting station is locking this object)

    n_of_stations: int  # number of transmitting stations in the channel
    n_of_eNB: int
    backoffs: Dict[int, Dict[int, int]]
    airtime_data: Dict[str, int]
    airtime_control: Dict[str, int]
    airtime_data_NR: Dict[str, int]
    airtime_control_NR: Dict[str, int]

    tx_list: List[Station] = field(default_factory=list)  # transmitting stations in the channel
    back_off_list: List[Station] = field(default_factory=list)  # stations in backoff phase
    tx_list_NR: List[Gnb] = field(default_factory=list)  # transmitting stations in the channel
    back_off_list_NR: List[Gnb] = field(default_factory=list)  # stations in backoff phase

    failed_transmissions: int = 0  # total failed transmissions
    succeeded_transmissions: int = 0  # total succeeded transmissions

    # Stats for individual categories

    succeeded_transmissions_be: int = 0
    succeeded_transmissions_bg: int = 0
    succeeded_transmissions_vc: int = 0
    succeeded_transmissions_vd: int = 0

    succeeded_transmissions_c1: int = 0
    succeeded_transmissions_c2: int = 0
    succeeded_transmissions_c3: int = 0
    succeeded_transmissions_c4: int = 0

    latency_wifi: List[complex] = field(default_factory=list)
    latency_nru: List[complex] = field(default_factory=list)

    latency_be: List[complex] = field(default_factory=list)
    latency_bg: List[complex] = field(default_factory=list)
    latency_vc: List[complex] = field(default_factory=list)
    latency_vd: List[complex] = field(default_factory=list)

    latency_c1: List[complex] = field(default_factory=list)
    latency_c2: List[complex] = field(default_factory=list)
    latency_c3: List[complex] = field(default_factory=list)
    latency_c4: List[complex] = field(default_factory=list)

    rts_list: List[Station] = field(default_factory=list)
    succeeded_rts: int = 0
    failed_rts: int = 0

    bytes_sent: int = 0  # total bytes sent
    failed_transmissions_NR: int = 0  # total failed transmissions
    succeeded_transmissions_NR: int = 0  # total succeeded transmissions

@dataclass()
class Frame:
    frame_time: int  # time of the frame
    station_name: str  # name of the owning it station
    col: str  # output color
    data_size: int  # payload size
    t_start: int  # generation time
    number_of_retransmissions: int = 0  # retransmissions count
    t_end: int = None  # sent time
    t_to_send: int = None  # how much time it took to sent successfully

    def __repr__(self):
        return (self.col + "Frame: start=%d, end=%d, frame_time=%d, retransmissions=%d"
                % (self.t_start, self.t_end, self.t_to_send, self.number_of_retransmissions)
                )

@dataclass()
class Transmission_NR:
    transmission_time: int
    enb_name: str  # name of the owning it station
    col: str
    t_start: int  # generation time / transmision start (including RS)
    airtime: int  # time spent on sending data
    rs_time: int  # time spent on sending reservation signal before data
    number_of_retransmissions: int = 0
    t_end: int = None  # sent time / transsmision end = start + rs_time + airtime
    t_to_send: int = None
    collided: bool = False  # true if transmission colided with another one


def getWifiTimeCategories(number_of_stations,airtime_data,trafficType):
    airtime_values=list(airtime_data.values())

    if trafficType == "background":
        return sum(airtime_values[0:number_of_stations["backgroundStations"]])
    elif  trafficType == "bestEffort":
        return sum(airtime_values[number_of_stations["backgroundStations"]:number_of_stations["backgroundStations"]+number_of_stations["bestEffortStations"]])
    elif  trafficType == "video":
        return sum(airtime_values[number_of_stations["backgroundStations"]+number_of_stations["bestEffortStations"]:number_of_stations["backgroundStations"]+number_of_stations["bestEffortStations"]+number_of_stations["videoStations"]])
    elif trafficType == "voice":
        return sum(airtime_values[number_of_stations["backgroundStations"] + number_of_stations["bestEffortStations"] +
                   number_of_stations["videoStations"]:number_of_stations["backgroundStations"]+number_of_stations["bestEffortStations"]+number_of_stations["videoStations"]+number_of_stations["voiceStations"]])

def getNruTimeCategories(number_of_stations,airtime_data,trafficType):
    airtime_values=list(airtime_data.values())

    if trafficType == "class_1":
        return sum(airtime_values[0:number_of_stations["class_1"]])
    elif  trafficType == "class_2":
        return sum(airtime_values[number_of_stations["class_1"]:number_of_stations["class_1"]+number_of_stations["class_2"]])
    elif  trafficType == "class_3":
        return sum(airtime_values[number_of_stations["class_1"]+number_of_stations["class_2"]:number_of_stations["class_1"]+number_of_stations["class_2"]+number_of_stations["class_3"]])
    elif trafficType == "class_4":
        return sum(airtime_values[number_of_stations["class_1"]+number_of_stations["class_2"]+number_of_stations["class_3"]:number_of_stations["class_1"]+number_of_stations["class_2"]+number_of_stations["class_3"]+number_of_stations["class_4"]])


def run_simulation(
        number_of_stations: Dict[str,int],
        number_of_gnb: Dict[str,int],
        seed: int,
        simulation_time: int,
        config: Config,
        config_nr: Config_NR,
        backoffs: Dict[int, Dict[int, int]],
        airtime_data: Dict[str, int],
        airtime_control: Dict[str, int],
        airtime_data_NR: Dict[str, int],
        airtime_control_NR: Dict[str, int],
        poisson_lambda,
        transtime,
        Queue,
        distribution_k,
        RTS_threshold,
        wifi_standard,
        nMPDU,
        nSS,
        buffer_size,
):
    random.seed(seed)
    environment = simpy.Environment()
    channel = Channel(
        simpy.PreemptiveResource(environment, capacity=1),
        simpy.Resource(environment, capacity=1),
        simpy.Resource(environment, capacity=1),
        sum(number_of_stations.values()),
        sum(number_of_gnb.values()),
        backoffs,
        airtime_data,
        airtime_control,
        airtime_data_NR,
        airtime_control_NR
    )

    global RTS_global_flag
    RTS_global_flag = True
    standard = wifi_standard
    transtime = transtime
    nAMPDU  = nMPDU
    nSS = nSS

    # EDCA categories handling
    for i in range(1, sum(number_of_stations.values()) + 1):
        # 1st group - Background
        if i in range (1,number_of_stations["backgroundStations"]+1):
            config_local = Config(config.data_size, 15, 1023, config.r_limit, config.mcs,7,RTS_threshold,standard,nAMPDU,nSS)
            Station(environment, "Station {}".format(i), channel,transtime, config_local,simulation_time,poisson_lambda,backoffs={key: {1: 0} for key in range(1023 + 1)},Queue=Queue,buffer_size=buffer_size)
        # 2nd group - Best Effort
        elif i in range (number_of_stations["backgroundStations"]+1,number_of_stations["backgroundStations"]+number_of_stations["bestEffortStations"]+1):
            config_local = Config(config.data_size, config.cw_min, config.cw_max, config.r_limit, config.mcs,3,RTS_threshold,standard,nAMPDU,nSS)
            Station(environment, "Station {}".format(i), channel=channel, config=config_local,simulation_time=simulation_time,poisson_lambda=poisson_lambda,backoffs={key: {1: 0} for key in range(config.cw_max + 1)},transtime=transtime,Queue=Queue,buffer_size=buffer_size)
        # 3rd group - Video
        elif i in range (number_of_stations["backgroundStations"]+number_of_stations["bestEffortStations"]+1,number_of_stations["backgroundStations"]+number_of_stations["bestEffortStations"]+number_of_stations["videoStations"]+1):
            config_local = Config(config.data_size, 7, 15, config.r_limit, config.mcs, 2,RTS_threshold,standard,nAMPDU,nSS)
            Station(environment, "Station {}".format(i), channel,transtime, config_local,simulation_time,poisson_lambda,backoffs={key: {1: 0} for key in range(15 + 1)},Queue=Queue,buffer_size=buffer_size)
        # 4th group - Voice
        else:
            config_local = Config(config.data_size, 3,7, config.r_limit, config.mcs, 2,RTS_threshold,standard,nAMPDU,nSS)
            Station(environment, "Station {}".format(i), channel,transtime, config_local,simulation_time,poisson_lambda,backoffs={key: {1: 0} for key in range(7 + 1)},Queue=Queue,buffer_size=buffer_size)

    # NR-U categories handling
    for i in range(1, sum(number_of_gnb.values()) + 1):

        # 1st group - Class 1
        if i in range (1,number_of_gnb["class_1"]+1):
            config_nr_local = Config_NR(deter_period=config_nr.deter_period, observation_slot_duration=config_nr.synchronization_slot_duration,
                                        synchronization_slot_duration=config_nr.synchronization_slot_duration,max_sync_slot_desync=config_nr.max_sync_slot_desync,
                                        min_sync_slot_desync=config_nr.min_sync_slot_desync, M=1, cw_min=3, cw_max=7,retry_limit=config_nr.retry_limit,
                                        mcot=2)
            Gnb(environment, "Gnb {}".format(i), channel=channel, config_nr=config_nr_local, transtime=transtime,backoffs={key: {1: 0} for key in range(7 + 1)}, poisson_lambda=poisson_lambda, Queue=Queue,buffer_size=buffer_size)

        # 2nd group - Class 2
        elif i in range (number_of_gnb["class_1"]+1,number_of_gnb["class_1"]+number_of_gnb["class_2"]+1):
            config_nr_local = Config_NR(deter_period=config_nr.deter_period, observation_slot_duration=config_nr.synchronization_slot_duration,
                                        synchronization_slot_duration=config_nr.synchronization_slot_duration, max_sync_slot_desync=config_nr.max_sync_slot_desync,
                                        min_sync_slot_desync=config_nr.min_sync_slot_desync, M=1, cw_min=7, cw_max=15, retry_limit=config_nr.retry_limit,
                                        mcot=3)
            Gnb(environment, "Gnb {}".format(i), channel=channel, config_nr=config_nr_local, transtime=transtime,backoffs={key: {1: 0} for key in range(15 + 1)}, poisson_lambda=poisson_lambda, Queue=Queue,buffer_size=buffer_size)

        # 3rd group - Class 3
        elif i in range (number_of_gnb["class_1"]+number_of_gnb["class_2"]+1,number_of_gnb["class_1"]+number_of_gnb["class_2"]+number_of_gnb["class_3"]+1):
            config_nr_local = Config_NR(deter_period=config_nr.deter_period, observation_slot_duration=config_nr.synchronization_slot_duration,
                                        synchronization_slot_duration=config_nr.synchronization_slot_duration, max_sync_slot_desync=config_nr.max_sync_slot_desync,
                                        min_sync_slot_desync=config_nr.min_sync_slot_desync, M=3, cw_min=15, cw_max=63, retry_limit=config_nr.retry_limit,
                                        mcot=3)
            Gnb(environment, "Gnb {}".format(i), channel=channel, config_nr=config_nr_local, transtime=transtime,backoffs={key: {1: 0} for key in range(63 + 1)}, poisson_lambda=poisson_lambda, Queue=Queue,buffer_size=buffer_size)

        # 4th group - Class 4
        else:
            config_nr_local = Config_NR(deter_period=config_nr.deter_period, observation_slot_duration=config_nr.synchronization_slot_duration,
                                        synchronization_slot_duration=config_nr.synchronization_slot_duration, max_sync_slot_desync=config_nr.max_sync_slot_desync,
                                        min_sync_slot_desync=config_nr.min_sync_slot_desync, M=7, cw_min=15, cw_max=1023, retry_limit=config_nr.retry_limit,
                                        mcot=8)
            Gnb(environment, "Gnb {}".format(i), channel=channel, config_nr=config_nr_local, transtime=transtime,backoffs={key: {1: 0} for key in range(1023 + 1)}, poisson_lambda=poisson_lambda, Queue=Queue,buffer_size=buffer_size)


    # for i in range(1, number_of_gnb + 1):
    #     Gnb(environment, "Gnb {}".format(i), channel=channel, config_nr=config_nr,transtime=transtime,backoffs = {key: {1: 0} for key in range(1023 + 1)},poisson_lambda=poisson_lambda,Queue=Queue,buffer_size=buffer_size)

    environment.run(until=simulation_time * 1000000)

    if sum(number_of_stations.values()) != 0:
        if (channel.failed_transmissions + channel.succeeded_transmissions) != 0:
            p_coll = "{:.4f}".format(
                channel.failed_transmissions / (channel.failed_transmissions + channel.succeeded_transmissions))
        else:
            p_coll = 0
    else:
        p_coll = 0

    if sum(number_of_gnb.values()) != 0:
        if (channel.failed_transmissions_NR + channel.succeeded_transmissions_NR) != 0:
            p_coll_NR = "{:.4f}".format(
                channel.failed_transmissions_NR / (channel.failed_transmissions_NR + channel.succeeded_transmissions_NR))
        else:
            p_coll_NR = 0
    else:
        p_coll_NR = 0

    channel_occupancy_time = 0
    channel_efficiency = 0
    channel_occupancy_time_NR = 0
    channel_efficiency_NR = 0
    time = simulation_time * 1000000

    for i in range(1, sum(number_of_stations.values()) + 1):
        channel_occupancy_time += channel.airtime_data["Station {}".format(i)] + channel.airtime_control["Station {}".format(i)]
        channel_efficiency += channel.airtime_data["Station {}".format(i)]

    for i in range(1, sum(number_of_gnb.values()) + 1):
        channel_occupancy_time_NR += channel.airtime_data_NR["Gnb {}".format(i)] + channel.airtime_control_NR["Gnb {}".format(i)]
        channel_efficiency_NR += channel.airtime_data_NR["Gnb {}".format(i)]

    # General metrics calculation
    normalized_channel_occupancy_time = channel_occupancy_time / time
    normalized_channel_efficiency = channel_efficiency / time
    normalized_channel_occupancy_time_NR = channel_occupancy_time_NR / time
    normalized_channel_efficiency_NR = channel_efficiency_NR / time
    normalized_channel_occupancy_time_all = (channel_occupancy_time + channel_occupancy_time_NR) / time
    normalized_channel_efficiency_all = (channel_efficiency + channel_efficiency_NR) / time
    throughput=(channel.succeeded_transmissions * config.data_size * 8) / (simulation_time * 1000000)

    # EDCA throughput calculation
    thrpt_vc = (channel.succeeded_transmissions_vc * config.data_size * 8) / (simulation_time * 1000000)
    thrpt_vd = (channel.succeeded_transmissions_vd * config.data_size * 8) / (simulation_time * 1000000)
    thrpt_be = (channel.succeeded_transmissions_be * config.data_size * 8) / (simulation_time * 1000000)
    thrpt_bg = (channel.succeeded_transmissions_bg * config.data_size * 8) / (simulation_time * 1000000)

    # NR-U categories throughput calculation (FOR FUTURE EXTENSION)
    thrpt_c1 = (channel.succeeded_transmissions_c1 * 8) / (simulation_time * 1000000)
    thrpt_c2 = (channel.succeeded_transmissions_c2 * 8) / (simulation_time * 1000000)
    thrpt_c3 = (channel.succeeded_transmissions_c3 * 8) / (simulation_time * 1000000)
    thrpt_c4 = (channel.succeeded_transmissions_c4 * 8) / (simulation_time * 1000000)

    # Jain's fairness index calculation
    jain_dict = airtime_data
    jain_dict.update(airtime_data_NR)
    try:
        jain_fair_index= pow(sum(jain_dict.values()),2) / ( (sum(number_of_gnb.values()) + sum(number_of_stations.values()) ) * sum({k: pow(v,2) for k,v in jain_dict.items() }.values()))
    except:
        jain_fair_index = 0

    # EDCA airtime calculation
    beAirTime = getWifiTimeCategories(number_of_stations,airtime_data,"bestEffort") / (simulation_time * 1000000)
    vdAirTime = getWifiTimeCategories(number_of_stations,airtime_data,"video") / (simulation_time * 1000000)
    vcAirTime = getWifiTimeCategories(number_of_stations,airtime_data,"voice") / (simulation_time * 1000000)
    bgAirTime = getWifiTimeCategories(number_of_stations,airtime_data,"background") / (simulation_time * 1000000)

    # NR-U airtime calculation
    c1AirTime = getNruTimeCategories(number_of_gnb, airtime_data_NR, "class_1") / (simulation_time * 1000000)
    c2AirTime = getNruTimeCategories(number_of_gnb, airtime_data_NR, "class_2") / (simulation_time * 1000000)
    c3AirTime = getNruTimeCategories(number_of_gnb, airtime_data_NR, "class_3") / (simulation_time * 1000000)
    c4AirTime = getNruTimeCategories(number_of_gnb, airtime_data_NR, "class_4") / (simulation_time * 1000000)

    # WiFi latency calculation
    avg_latency_wifi = ((sum(channel.latency_wifi))/(len(channel.latency_wifi)))/ (1000000)

    # WiFi EDCA latency calculation
    avg_latency_be = ((sum(channel.latency_be))   / (len(channel.latency_be)+1)) /  (1000000)
    avg_latency_bg = ((sum(channel.latency_bg))   / (len(channel.latency_bg)+1)) /  (1000000)
    avg_latency_vd = ((sum(channel.latency_vd))   / (len(channel.latency_vd)+1)) /  (1000000)
    avg_latency_vc = ((sum(channel.latency_vc))   / (len(channel.latency_vc)+1)) /  (1000000)

    # NR-U latency calculation
    try:
        avg_latency_nru = (sum(channel.latency_nru)/(len(channel.latency_nru)))/ (1000000)
    except:
        avg_latency_nru = None

    # NR-U categories latency calculation
    avg_latency_c1 = ((sum(channel.latency_c1)) / (len(channel.latency_c1) + 1)) / (1000000)
    avg_latency_c2 = ((sum(channel.latency_c2)) / (len(channel.latency_c2) + 1)) / (1000000)
    avg_latency_c3 = ((sum(channel.latency_c3)) / (len(channel.latency_c3) + 1)) / (1000000)
    avg_latency_c4 = ((sum(channel.latency_c4)) / (len(channel.latency_c4) + 1)) / (1000000)

    # WiFi jitter calculation
    jitter_wifi = numpy.var(channel.latency_wifi)/ (1000000)

    # EDCA jitter calculation
    jitter_be = numpy.var(channel.latency_be)/ (1000000)
    jitter_bg = numpy.var(channel.latency_bg)/ (1000000)
    jitter_vd = numpy.var(channel.latency_vd)/ (1000000)
    jitter_vc = numpy.var(channel.latency_vc)/ (1000000)

    # NR-U latency calculation
    jitter_nru = numpy.var(channel.latency_nru)/ (1000000)

    # NR-U categories latency calculation
    jitter_c1 = numpy.var(channel.latency_c1)/ (1000000)
    jitter_c2 = numpy.var(channel.latency_c2)/ (1000000)
    jitter_c3 = numpy.var(channel.latency_c3)/ (1000000)
    jitter_c4 = numpy.var(channel.latency_c4)/ (1000000)

    # Printing results
    print("------------------------------------------------------------------------------------------")
    print("")
    print("THROUGHPUT")
    print(" T_VC: ", thrpt_vc, " T_VD: ",thrpt_vd, " T_BE: ",thrpt_be, " T_BG: ",thrpt_bg)
    print(" T_C1: ", thrpt_c1, " T_C2: ", thrpt_c2, " T_C3: ", thrpt_c3, " T_C4: ", thrpt_c4)
    print("")
    print("AIR TIME")
    print(" BE: ",beAirTime," BG: ",bgAirTime," VD: ",vdAirTime," VC: ",vcAirTime)
    print(" C1: ", c1AirTime, "C2: ", c2AirTime, "C3: ", c3AirTime, "C4: ", c4AirTime)
    print("")
    print("LATENCY")
    print("WiFi: ", avg_latency_wifi)
    print("BG: ",avg_latency_bg, "BE: ",avg_latency_be, "VD: ",avg_latency_vd, "VO: ",avg_latency_vc)
    print("NR-U: ", avg_latency_nru)
    print("C1: ", avg_latency_c1, "C2: ", avg_latency_c2, "C3: ", avg_latency_c3, "C4: ", avg_latency_c4)
    print("")
    print("JITTER")
    print("WiFi: ", jitter_wifi)
    print("BG: ", jitter_bg, "BE: ", jitter_be, "VD: ", jitter_vd, "VO: ", jitter_vc)
    print("NR-U: ", jitter_nru)
    print("C1: ", jitter_c1, "C2: ", jitter_c2, "C3: ", jitter_c3, "C4: ", jitter_c4)
    print("")
    print(
        f"SEED = {seed} N_stations:={sum(number_of_stations.values())} N_gNB:={sum(number_of_gnb.values())}  CW_MIN = {config.cw_min} CW_MAX = {config.cw_max} "
        f"WiFi pcol:={p_coll} WiFi cot:={normalized_channel_occupancy_time} WiFi eff:={normalized_channel_efficiency} "
        f"gNB pcol:={p_coll_NR} gNB cot:={normalized_channel_occupancy_time_NR} gNB eff:={normalized_channel_efficiency_NR} "
        f" all cot:={normalized_channel_occupancy_time_all} all eff:={normalized_channel_efficiency_all}"
    )
    print(f" Wifi succ: {channel.succeeded_transmissions} fail: {channel.failed_transmissions}")
    print(f" NR succ: {channel.succeeded_transmissions_NR} fail: {channel.failed_transmissions_NR}")
    print("WiFi throughput", (channel.succeeded_transmissions * config.data_size * 8) / (simulation_time * 1000000))
    print("payload:",config.data_size)
    print("lambda:", poisson_lambda)
    print("sync",config_nr.synchronization_slot_duration)
    print("JFE: ", jain_fair_index)
    print("distribution_k: ", distribution_k)
    print("MCS: ",config.mcs)
    print("nAMPDU: ", nAMPDU)
    print("nSS: ", nSS)
    print("buffer: ", buffer_size)
    print("------------------------------------------------------------------------------------------")
    print("")

    # SAVING RESULTS TO THE CSV
    write_header = True
    if os.path.isfile(output_csv):
        write_header = False
    with open(output_csv, mode='a', newline="") as result_file:
        result_adder = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        firstliner='Seed,WiFi,Gnb,ChannelOccupancyWiFi,ChannelEfficiencyWiFi,PcollWiFi,ChannelOccupancyNR,ChannelEfficiencyNR,PcollNR,ChannelOccupancyAll,ChannelEfficiencyAll,' \
                   'Throughput,Payload,SimulationTime,JainFairIndex,beAirTime,vdAirTime,vcAirTime,bgAirTime,lambda,thrpt_vc,thrpt_vd,thrpt_be,thrpt_bg,cw_min,mcs,retryLimit,sync,' \
                   'lenLte,distribution_k,nMPDU,nss,buffer,c1AirTime,c2AirTime,c3AirTime,c4AirTime,thrpt_c1,thrpt_c2,thrpt_c3,thrpt_c4,' \
                   'latency_wifi,latency_nru,latency_bg,latency_be,latency_vd,latency_vc,latency_c1,latency_c2,latency_c3,latency_c4,jitter_wifi,jitter_be,jitter_bg,jitter_vd,jitter_vc,' \
                   'jitter_nru,jitter_c1,jitter_c2,jitter_c3,jitter_c4'

        if write_header:
            result_adder.writerow([firstliner.strip('"')])

        result_adder.writerow(
            [seed, sum(number_of_stations.values()), sum(number_of_gnb.values()), normalized_channel_occupancy_time, normalized_channel_efficiency,
             p_coll,
             normalized_channel_occupancy_time_NR, normalized_channel_efficiency_NR, p_coll_NR,
             normalized_channel_occupancy_time_all, normalized_channel_efficiency_all,throughput,
             config.data_size,simulation_time,jain_fair_index,beAirTime,vdAirTime,vcAirTime,bgAirTime,poisson_lambda,
             thrpt_vc,thrpt_vd,thrpt_be,thrpt_bg,config.cw_min,config.mcs,config.r_limit,config_nr.synchronization_slot_duration,
             transtime,distribution_k,nMPDU,nSS,buffer_size,c1AirTime,c2AirTime,c3AirTime,
             c4AirTime,thrpt_c1,thrpt_c2,thrpt_c3,thrpt_c4,avg_latency_wifi,avg_latency_nru,avg_latency_bg,avg_latency_be,
             avg_latency_vd,avg_latency_vc,avg_latency_c1,avg_latency_c2,avg_latency_c3,avg_latency_c4,jitter_wifi,jitter_be,jitter_bg,jitter_vd,jitter_vc,jitter_nru,jitter_c1,
             jitter_c2,jitter_c3,jitter_c4])













