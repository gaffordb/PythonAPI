#!/home/ubuntu/anaconda3/bin/python

import os
import lgsvl

SIMULATOR_HOST = os.environ.get("SIMULATOR_HOST", "127.0.0.1")
SIMULATOR_PORT = int(os.environ.get("SIMULATOR_PORT", 8181))
BRIDGE_HOST = os.environ.get("BRIDGE_HOST", "127.0.0.1")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", 9090))

sim = lgsvl.Simulator(SIMULATOR_HOST, SIMULATOR_PORT)
if sim.current_scene == "BorregasAve":
    sim.reset()
else:
    sim.load("BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]

ego = sim.add_agent("25f1d3b4-c3d2-41fe-b855-bccda6267e20", lgsvl.AgentType.EGO, state)
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

dv.setup_apollo(destination.position.x, destination.position.z, modules)

#input("Press Enter to start the simulation.")

sim.run()
