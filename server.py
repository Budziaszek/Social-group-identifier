from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from model import SiteModel

chart = ChartModule([], data_collector_name='datacollector')

model_params = {}

server = ModularServer(SiteModel, [chart], "Site Model", model_params)

from server import server
server.port = 8521 # The default
server.launch()