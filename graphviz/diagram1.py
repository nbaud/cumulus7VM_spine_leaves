from graphviz import Digraph

dot = Digraph('Network', engine='dot')
dot.attr(rankdir='TB', splines='line')
dot.node_attr.update(shape='record', style='filled', fillcolor='lightgrey', height='0.5')

# Corrected node definitions using HTML-like labels
dot.node('spine01', label='<spine01|10.1.0.1/32>')
dot.node('spine02', label='<spine02|10.1.0.2/32>')
dot.node('leaf01', label='<leaf01|10.0.0.1/32>')
dot.node('leaf02', label='<leaf02|10.0.0.2/32>')
dot.node('leaf03', label='<leaf03|10.0.0.3/32>')

# Define connections
# Note: Adjust the label placement and connection details as needed
connections = [
    ('leaf01', 'spine01', '10.1.1.1/30 - 10.1.1.2/30'),
    ('leaf01', 'spine02', '10.2.1.1/30 - 10.2.1.2/30'),
    ('leaf02', 'spine01', '10.1.2.1/30 - 10.1.2.2/30'),
    ('leaf02', 'spine02', '10.2.2.1/30 - 10.2.2.2/30'),
    ('leaf03', 'spine01', '10.1.3.1/30 - 10.1.3.2/30'),
    ('leaf03', 'spine02', '10.2.3.1/30 - 10.2.3.2/30'),
]

for src, dst, label in connections:
    dot.edge(src, dst, label=label, arrowhead='none')

# Additional layout adjustments
dot.body.append('{ rank=same; spine01; spine02 }')
dot.body.append('{ rank=same; leaf01; leaf02; leaf03 }')

# Render and save the diagram
output_path = 'adjusted_network_diagram'
dot.render(output_path, format='png', cleanup=True)

output_path + '.png'

