#!/home/ubuntu/anaconda3/bin/python

import os
import lgsvl
import time
import logging
from environs import Env

MAX_EGO_SPEED = 11.111  # (40 km/h, 25 mph)
MAX_POV_SPEED = 8.889  # (32 km/h, 20 mph)
INITIAL_HEADWAY = 130  # spec says >30m
SPEED_VARIANCE = 4
TIME_LIMIT = 100
TIME_DELAY = 3

SIMULATOR_HOST = os.environ.get("SIMULATOR_HOST", "127.0.0.1")
SIMULATOR_PORT = int(os.environ.get("SIMULATOR_PORT", 8181))
BRIDGE_HOST = os.environ.get("BRIDGE_HOST", "127.0.0.1")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", 9090))

sim = lgsvl.Simulator(SIMULATOR_HOST, SIMULATOR_PORT)
if sim.current_scene == "BorregasAve":
    sim.reset()
else:
    sim.load("BorregasAve", seed=314)

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]

# uncomment for base apollo agent
ego = sim.add_agent("2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921", lgsvl.AgentType.EGO, state)
ego.connect_bridge(BRIDGE_HOST, BRIDGE_PORT)

# Dreamview setup
dv = lgsvl.dreamview.Connection(sim, ego, BRIDGE_HOST)
dv.set_hd_map('Borregas Ave')
dv.set_vehicle('Lincoln2017MKZ_LGSVL')
modules = [
    'Localization',
    'Perception',
    'Transform',
    'Routing',
    'Prediction',
    'Planning',
    'Traffic Light',
    'Control'
]
destination = spawns[0].destinations[0]

#state.transform.rotation.y = 180

#ped_state = state
#ped_state.transform.position.x = ped_state.transform.position.x + 100

npc_state = lgsvl.AgentState()
state.transform.position = lgsvl.Vector(1.8687, -2.1091, -23.6003)
npc = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npc_state)

dv.setup_apollo(destination.position.x, destination.position.z, modules)

sim.add_random_agents(lgsvl.AgentType.NPC)
#input("Press Enter to start the simulation.")
sim.run()
print("is this synchronous?")
'''
try:
    #    input("Press Enter to start the simulation.")
    t0 = time.time()
    sim.run(TIME_DELAY)
    while True:
        egoCurrentState = ego.state
        print(ego.state)
        sim.run(10)
        if time.time() - t0 > TIME_LIMIT:
            break
except lgsvl.evaluator.TestException as e:
    exit("FAILED: {}".format(e))
'''
