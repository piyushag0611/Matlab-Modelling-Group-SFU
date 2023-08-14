import numpy as np
import matplotlib.pyplot as plt

def generate_network():
    syllables = ['bepg', 'phit', 'bepph', 'git']
    segments = [['b_o', 'g_o', 't_o', 'ph_o'], ['ep_n', 'i_n'], ['b_c', 'g_c', 't_c', 'ph_c']]
    syllablification = ['bepg_phit', 'bepph_git']
    network_nodes = {}
    network_nodes['bepg'] = ['b_o', 'ep_n', 'g_c']
    network_nodes['phit'] = ['ph_o', 'i_n', 't_c']
    network_nodes['bepph'] = ['b_o', 'ep_n', 'ph_c']
    network_nodes['git'] = ['g_o', 'i_n', 't_c']
    network_nodes['b_o'] = ['bepg', 'bepph', 'bepg_phit', 'bepph_git']
    network_nodes['g_o'] = ['git', 'bepph_git']
    network_nodes['ph_o'] = ['phit', 'bepg_phit']
    network_nodes['ep_n'] = ['bepg', 'bepph', 'bepg_phit', 'bepph_git']
    network_nodes['i_n'] = ['phit', 'git', 'bepg_phit', 'bepph_git']
    network_nodes['g_c'] = ['bepg', 'bepg_phit']
    network_nodes['t_c'] = ['phit', 'git', 'bepg_phit', 'bepph_git']
    network_nodes['ph_c'] = ['bepph', 'bepph_git']
    network_nodes['bepg_phit'] = ['b_o', 'ph_o', 'ep_n', 'i_n', 'g_c', 't_c']
    network_nodes['bepph_git'] = ['b_o', 'g_o', 'ep_n', 'i_n', 'ph_c', 't_c']
    activations = {}
    for key in network_nodes:
        activations[key] = [0]
    return network_nodes, activations

def simulate_network(network, activations, params):
    (n, p, q, std1, std2, inhibition, seed) = params
    random_gen = np.random.default_rng(seed)
    for t in range(n):
        for node in network:
            neighbors_activation = 0
            for neighbor in network[node]:
                neighbors_activation += p*max(activations[neighbor][-1], 0)
            noise1 = random_gen.normal(scale=std1)
            if(node=='bepg_phit'):
                activations[node].append(neighbors_activation+noise1+(1-q)*activations[node][-1]-inhibition)
            else:
                activations[node].append(neighbors_activation+noise1+(1-q)*activations[node][-1])
            noise2 = random_gen.normal(scale=std2*max(activations[node][-1], 0))
            activations[node][-1] += noise2

    return activations

def main():
    network, activations = generate_network()
    param = [10, 0.1, 0.5, 0.01, 0.16, 0.1, 1]
    activations['bepg'] = [10]
    activations['phit'] = [10]
    activations = simulate_network(network, activations, param)
    plt.plot(range(param[0]+1), activations['bepg'], label='bepg')
    plt.plot(range(param[0]+1), activations['bepph'], label='bepph')
    plt.xlabel("Time-step")
    plt.ylabel("Excitation value")
    plt.title("Excitations for bepg vs bepph")
    plt.savefig("exc1.png")
    plt.figure()
    plt.plot(range(param[0]+1), activations['phit'], label='phit')
    plt.plot(range(param[0]+1), activations['git'], label='git')
    plt.xlabel("Time-step")
    plt.ylabel("Excitation value")
    plt.title("Excitations for phit vs git")
    plt.savefig("exc2.png")
    plt.figure()
    plt.plot(range(param[0]+1), activations['bepg_phit'], label='bepg_phit')
    plt.plot(range(param[0]+1), activations['bepph_git'], label='bepph_git')
    plt.xlabel("Time-step")
    plt.ylabel("Excitation value")
    plt.title("Excitations for bepg_phit vs bepph_git")
    plt.savefig("exc3.png")
    plt.legend()
    plt.show()

if(__name__=="__main__"):
    main()

    











