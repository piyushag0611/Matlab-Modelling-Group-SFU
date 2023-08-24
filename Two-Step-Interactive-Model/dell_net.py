import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Speech-error-Rate

def generate_network(choice):
    onsets = ['f', 'l', 'd', 'k', 'm']
    words = ['fog', 'dog', 'cat', 'mat', 'log']
    #This is to incorporate the two different neighborhoods.
    if(choice==0):
        words.append('hat')
        sem_nodes  = 57
        onsets.append('h')
    else:
        words.append('rat')
        sem_nodes  = 54
        onsets.append('r')
    
    network_nodes = {}
    nodes = list(range(sem_nodes)) + words + onsets + ['ae', 'o'] + ['t', 'g']
    for node in nodes:
        network_nodes[node] = []

    for i in range(10):
        if(i>=2 and i<=4):
            network_nodes[i].append('cat')
            network_nodes['cat'].append(i)
            network_nodes[i].append('dog')
            network_nodes['dog'].append(i)
            if(choice==1):
                network_nodes[i].append('rat')
                network_nodes['rat'].append(i)
        else:
            network_nodes[i].append('cat')
            network_nodes['cat'].append(i)
    
    if(choice==0):
        for i in range(10, 57):
            if(i>=10 and i<17):
                node_word = 'dog'
            elif(i>=17 and i<27):
                node_word = 'hat'
            elif(i>=27 and i<37):
                node_word = 'mat'
            elif(i>=37 and i<47):
                node_word = 'log'
            else:
                node_word = 'fog'
            network_nodes[i].append(node_word)
            network_nodes[node_word].append(i)
    else:
        for i in range(10, 54):
            if(i>=10 and i<17):
                node_word = 'dog'
            elif(i>=17 and i<24):
                node_word = 'rat'
            elif(i>=24 and i<34):
                node_word = 'mat'
            elif(i>=34 and i<44):
                node_word = 'log'
            else:
                node_word = 'fog'
            network_nodes[i].append(node_word)
            network_nodes[node_word].append(i)

    for word in words:
        if(word=='cat'):
            onset = 'k'
        else:
            onset= word[0]
        network_nodes[onset].append(word)
        network_nodes[word].append(onset)
        if(word[1]=='a'):
            vowel='ae'
        else:
            vowel='o'
        network_nodes[vowel].append(word)
        network_nodes[word].append(vowel)
        coda = word[2]
        network_nodes[coda].append(word)
        network_nodes[word].append(coda)

    return network_nodes

def simulate_network(network, activations, params):
    (p, q, std1, std2, n, seed, start) = params
    random_gen = np.random.default_rng(seed)
    for t in range(1+start, 1+start+n):
        for node in network:
            neighbors_activation = 0
            for neighbor in network[node]:
                neighbors_activation += p*max(activations.loc[t-1, neighbor], 0)
            noise1 = random_gen.normal(scale=std1)
            activations.loc[t, node] = (neighbors_activation+noise1+(1-q)*activations.loc[t-1, node])
            noise2 = random_gen.normal(scale=std2*max(activations.loc[t, node], 0))
            activations.loc[t, node] += noise2

    return activations

def generate_result(cat, p_, q_, seed_):
    network = generate_network(cat)
    if(cat==0):
        lemmas = ['fog', 'dog', 'cat', 'mat', 'log', 'hat']
        onsets = ['f', 'd', 'k', 'm', 'l', 'h']
    else:
        lemmas = ['fog', 'dog', 'cat', 'mat', 'log', 'rat']
        onsets = ['f', 'd', 'k', 'm', 'l', 'r']
    params = (p, q, std1, std2, n, seed, start) = (p_, q_, 0.01, 0.16, 8, seed_, 0)
    activation_values = pd.DataFrame(np.zeros((2*n+1, len(network))), columns=network.keys())
    for i in range(10):
        activation_values.loc[0, i] = 10
    activation_values = simulate_network(network, activation_values, params)
    chosen_lemma = activation_values.loc[n, lemmas].idxmax()
    activation_values.loc[n, chosen_lemma] = 100
    params = (0.1, 0.5, 0.01, 0.16, 8, seed_, n)
    activation_values = simulate_network(network, activation_values, params)
    chosen_onset = activation_values.loc[2*n, onsets].idxmax()
    chosen_vowel = activation_values.loc[2*n, ['ae', 'o']].idxmax()
    chosen_coda = activation_values.loc[2*n, ['g', 't']].idxmax()
    if(chosen_onset=='k'):
        chosen_onset = 'c'
    if(chosen_vowel=='ae'):
        chosen_vowel = 'a'
    formed_word = chosen_onset+chosen_vowel+chosen_coda
    activation_values.to_csv('act_val.csv')
    return formed_word
    

def get_error_results(res1, res2, runs):
    correct = (0.9*res1['cat'] + 0.1*res2['cat'])
    semantic = (0.9*res1['dog'] + 0.1*res2['dog'])
    mixed = (0.1*res2['rat'])
    formal = 0
    if('mat' in res1):
        formal += 0.9*res1['mat']
    if('hat' in res1):
        formal += 0.9*res1['hat']
    if('mat' in res2):
        formal += 0.1*res2['mat']
    unrelated = 0
    if('log' in res1):
        unrelated += 0.9*res1['log']
    if('log' in res2):
        unrelated += 0.1*res1['log']
    if('fog' in res1):
        unrelated += 0.9*res1['fog']
    if('fog' in res1):
        unrelated += 0.1*res1['fog']
    return (np.round(np.array([correct/runs, semantic/runs, formal/runs, 1-(correct+semantic+formal+mixed+unrelated)/runs, mixed/runs, unrelated/runs]), 3))

def main():
    runs = 1000
    p = 0.1
    q = 0.5
    answers1 = []
    answers2 = []
    for seed in range(runs):
        answers1.append(generate_result(0, p, q, seed))
        answers2.append(generate_result(1, p, q, seed))
    res1 = pd.Series(answers1).value_counts()
    res2 = pd.Series(answers2).value_counts()
    (correct_, semantic_, formal_, nonwords_, mixed_, unrelated_) = get_error_results(res1, res2, runs)
    print('Correct:', np.round(correct_, 3))
    print('Semantic:', np.round(semantic_, 3))
    print('Mixed:', np.round(mixed_, 3))
    print('Formal:', np.round(formal_, 3))
    print('Unrelated:', np.round(unrelated_, 3))
    print('Nonword:', np.round(nonwords_, 3))

if(__name__=="__main__"):
    main()


