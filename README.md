## 5G-Coex-SimPy

### Introduction

This is 5G-Coex-SimPy discrete-event simulator based on the SimPy Python library that allows to study and research coexistence between WiFi and NR-U (New Radio Unlicensed) technologies. 

### Engineer's (BSc) Thesis 

```
Validation and Extension of a WiFi and NR-U Coexistence Channel Access Simulator based on the Python SimPy Library
```

My Bachelor thesis was focused on the research and validation of existing functionalities as well as extending it with the following features:

- EDCA
- Non-saturated traffic generation
- Airtime fairness
- Random packet size generation
- RTS/CTS
- 802.11ac

### Master's (MSc) Thesis

```
Simulation Analysis of QoS in Wi-Fi and NR-U Network Coexistence
Scenarios
```

My Master thesis is focused on the Quality of Service aspects of the above mentioned technologies coexisting in the same band. So far, I have managed to enrich the simulator with the following functionalities:

- NR-U Access Categories
- Arbitrary buffer size management
- QoS metrics (throughput, latency, Packet Loss Ratio, jitter)

### How to run?

In order to properly run 5G-Coex-SimPy, an IDE (like PyCharm) is needed to smoothly install all the dependencies and libraries. However, you can also install the dependencies via the command line with pip. The 5G-Coex-SimPy consists of the following scripts:


- *client_coex.py* - configuring and running simmulations
- *Coexistence.py* and *Times.py* - simulation logic 
- *resultAnalysis.py* - results processing and visualization 



