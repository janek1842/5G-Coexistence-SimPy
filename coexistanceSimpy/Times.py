import math
import string

MCS = {
    0: [6, 6],
    1: [9, 6],
    2: [12, 12],
    3: [18, 12],
    4: [24, 24],
    5: [36, 24],
    6: [48, 24],
    7: [54, 24],
}

MCS_ac = {
    0: [6.5, 6],
    1: [13, 12],
    2: [19.5, 12],
    3: [26, 24],
    4: [39, 24],
    5: [52, 24],
    6: [58.5, 24],
    7: [65, 24],
    8: [78, 24],
}

class Times:

    t_slot = 9  # [us]
    t_sifs = 16  # [us]

    ack_timeout = 44  # [us]

    # Mac overhead
    mac_overhead = (40) * 8  # [b]

    # ACK size
    ack_size = 14 * 8  # [b]

    t_difs= 16 + 3*9

    # overhead
    _overhead = 22  # [b]


    def __init__(self, payload: int = 1472, mcs: int = 7, aifsn: int = 3,standard: string = "802.11a",nss: int=1):
        self.payload = payload
        self.mcs = mcs
        self.nss = nss
        # OFDM parameters

        if standard == "802.11a":
            self.phy_data_rate = MCS[mcs][0] * pow(10, -6)  # [Mb/us] Possible values 6, 9, 12, 18, 24, 36, 48, 54
            self.phy_ctr_rate = MCS[mcs][1] * pow(10, -6)  # [Mb/us]
            self.data_rate = MCS[mcs][0]  # [b/us]
            self.ctr_rate = MCS[mcs][1]  # [b/us]

        elif standard == "802.11ac":
            self.phy_data_rate = nss*MCS_ac[mcs][0] * pow(10, -6)  # [Mb/us]
            self.phy_ctr_rate = MCS_ac[mcs][1] * pow(10, -6)  # [Mb/us]
            self.data_rate = nss*MCS_ac[mcs][0]  # [b/us]
            self.ctr_rate = MCS_ac[mcs][1]  # [b/us]

        self.n_data = 4 * self.phy_data_rate  # [b/symbol]
        self.n_ctr = 4 * self.phy_ctr_rate  # [b/symbol]
        self.ofdm_preamble = 16  # [us]
        self.ofdm_signal = 24 / self.ctr_rate  # [us]

        self.aifsn = aifsn
        t_slot = 9  # [us]
        t_sifs = 16  # [us]

        self.t_difs = aifsn * t_slot + t_sifs  # [us]

    # Data frame time
    def get_ppdu_frame_time(self,k):
        msdu = self.payload * 8  # [b]

        # MacFrame
        mac_frame =  k*Times.mac_overhead + msdu  # [b]

        # PPDU Padding
        ppdu_padding = math.ceil(
            (Times._overhead + mac_frame) / self.n_data
        ) * self.n_data - (Times._overhead + mac_frame)

        # CPSDU Frame
        cpsdu = Times._overhead + mac_frame + ppdu_padding  # [b]

        # PPDU Frame
        ppdu = self.ofdm_preamble + self.ofdm_signal + cpsdu / self.data_rate  # [us]

        ppdu_tx_time = math.ceil(ppdu)
        #print(ppdu_tx_time)

        return ppdu_tx_time  # [us]

    # ACK frame time with SIFS
    def get_ack_frame_time(self):
        ack = Times._overhead + Times.ack_size  # [b]
        ack = self.ofdm_preamble + self.ofdm_signal + ack / self.ctr_rate  # [us]
        ack_tx_time = Times.t_sifs + ack
        return math.ceil(ack_tx_time)
        #return 28+16

    def get_rts_cts_time(self):
        return 2 * Times.t_sifs + (14 * 8 / self.ctr_rate) + Times.t_difs + (20 * 8 / self.ctr_rate)



