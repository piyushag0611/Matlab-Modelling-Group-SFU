import pandas as pd
from pathlib import Path

def equilibrium(query):
    infile = Path(__file__).parent / "jetsandshark.csv"
    js_data = pd.read_csv(infile)
    
    excitory_nodes = {}
    for i in range(27):
        for j in range(1, 6):
            if(js_data.iloc[i][0] in excitory_nodes):
                excitory_nodes[js_data.iloc[i][0]].append(js_data.iloc[i][j])
            else:
                excitory_nodes[js_data.iloc[i][0]] = [js_data.iloc[i][j]]
    
            if(js_data.iloc[i][j] in excitory_nodes):
                excitory_nodes[js_data.iloc[i][j]].append(js_data.iloc[i][0])
            else:
                excitory_nodes[js_data.iloc[i][j]] = [js_data.iloc[i][0]]
    
    inhibitory_nodes = {}
    for col in js_data.columns.values:
        nodes_ = set(list(js_data.iloc[:][col]))
        for entry in nodes_:
            inhibitory_nodes[entry] = []
            for cluster_mate in nodes_:
                if(cluster_mate!=entry):
                    inhibitory_nodes[entry].append(cluster_mate)
    
    activation_values = {}
    time = 200
    for key in excitory_nodes.keys():
        activation_values[key] = [-0.2]
    
    probe_ = {}
    for key in excitory_nodes.keys():
        probe_[key] = 0

    for key in query:
        probe_[key] = 0.2
    
    for i in range(1, time):
        for node in activation_values.keys():
            current_val = activation_values[node][i-1]
            input_ = probe_[node]
            for exc_node in excitory_nodes[node]:
                input_ += 0.05*activation_values[exc_node][i-1]
            for inhb_node in inhibitory_nodes[node]:
                input_ -= 0.03*activation_values[inhb_node][i-1]
            if(input_ >0):
                effect_ = (1-current_val)*input_
            else:
                effect_ = (current_val+0.2)*input_
            new_val = current_val + effect_ - 0.05*(current_val-0.1)
            activation_values[node].append(new_val)

    final_values = {}

    for node in activation_values.keys():
        final_values[node] = activation_values[node][-1]

    return final_values
    
    
