import pandas as pd
data = pd.read_csv('input.csv')
node_data = pd.read_csv('index.csv')

import holoviews as hv
from holoviews import opts, dim
import holoviews.plotting.bokeh
hv.extension('bokeh')
hv.output(size=200)

#add node labels
nodes = hv.Dataset(pd.DataFrame(node_data['nodes']), 'index')

#create chord object
chord = hv.Chord((data, nodes)).select(value=(5, None))

#customization of chart
chord.opts(
    opts.Layout(title="Chord Diagram Example"),     
    opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('Source').str(), 
    labels='nodes', node_color=dim('index').str())
)