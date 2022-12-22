from renderer import *
from magneticsources import *

system = System(8.85418782e-12, 0.04)
renderer = Renderer(system, 10, 10, 1, 200, 200)

renderer.launch()