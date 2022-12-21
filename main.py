from renderer import *
from magneticsources import *

system = System(8.85418782e-12, 0.04)
renderer = Renderer(system, 10, 10, 1.6, 400, 400)

renderer.system.add_source(Wire(0, 0, 0.5, 10))

renderer.launch()