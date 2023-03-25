network_nodes = containers.Map;
excitation_values = containers.Map;

for i=1:12
    str = string(i);
    network_nodes(str) = {};
    excitation_values(str) = {0};
end

words = {'fog', 'dog', 'cat', 'rat', 'mat'};
for i=1:length(words)
    word = words{i};
    network_nodes(word) = {};
    excitation_values(word) = {0};
end

onsets = {'f', 'r', 'd', 'k', 'm'};
for i=1:length(onsets)
    onset = onsets{i};
    network_nodes(onset) = {};
    excitation_values(onset) = {0};
end

vowels = {'ae', 'o'};
for i=1:length(vowels)
    vowel = vowels{i};
    network_nodes(vowel) = {};
    excitation_values(vowel) = {0};
end

codas = {'t', 'g'};
for i=1:length(codas)
    coda = codas{i};
    network_nodes(coda) = {};
    excitation_values(coda) = {0};
end

for i=2:10
    if(i>=4 && i<=6)
        str = string(i);
        network_nodes(str) = {'cat', 'dog', 'rat'};
        network_nodes('cat') = [network_nodes('cat'), str];
        network_nodes('dog') = [network_nodes('dog'), str];
        network_nodes('rat') = [network_nodes('rat'), str];
    else
        str = string(i);
        network_nodes(str) = {'cat'};
        network_nodes('cat') = [network_nodes('cat'), str];
    end
end

for i=1:length(words)
    word = words{i};
    if(strcmp(word, 'cat'))
        onset = 'k';
    else
        onset = word(1);
    end
    network_nodes(onset) = [network_nodes(onset), word];
    network_nodes(word) = [network_nodes(word), onset];
    if(word(2)=='a')
        vowel='ae';
    else
        vowel='o';
    end
    network_nodes(vowel) = [network_nodes(vowel), word];
    network_nodes(word) = [network_nodes(word), vowel];
    coda = word(3);
    network_nodes(coda) = [network_nodes(coda), word];
    network_nodes(word) = [network_nodes(word), coda];
end


q = 0.1;
p = 0.01;
n = 100;

rng('default');
std_dev1 = 0.001;
std_dev2 = 0.001;

for i = 1:10
    excitation_values(num2str(i)) = {10};
end


for t = 2:n-1
    keys = network_nodes.keys;
    for k = 1:numel(keys)
        key = keys{k};
        modifiers_ = 0;
        connections = network_nodes(key);
        for i = 1:numel(connections)
            connection = connections{i};
            neighbor_excitation_values = excitation_values(connection);
            neighbor_val = neighbor_excitation_values{end};
            if neighbor_val < 0
                continue;
            else
                modifiers_ = modifiers_ + p * neighbor_val;
            end
        end
        current_excitation_vals = excitation_values(key);
        current_val = current_excitation_vals{end};
        noise = randn() * std_dev1 + randn() * abs(std_dev2 * current_val);
        excitation_values(key) = [excitation_values(key),  current_val* (1-q) + modifiers_ + noise];
    end
end
