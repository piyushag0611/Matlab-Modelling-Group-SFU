js_data = readtable("C:\Spring Term\Matlab Modelling Group\jetsandshark.csv");
excitory_nodes = containers.Map;
for i = 1:27
    for j = 2:6
        ele1 = cell2mat(js_data{i, 1}(1));
        ele2 = cell2mat(js_data{i, j}(1));
        if isKey(excitory_nodes, ele1)
            excitory_nodes(ele1) = [excitory_nodes(ele1) {ele2}];
        else
            excitory_nodes(ele1) = {ele2};
        end

        if isKey(excitory_nodes, ele2)
            excitory_nodes(ele2) = [excitory_nodes(ele2) {ele1}];
        else
            excitory_nodes(ele2) = {ele1};
        end
    end
end
inhibitory_nodes = containers.Map;
for i = 1:6
    col = unique(table2array(js_data(:, i)));
    for j = 1:size(col, 1)
        ele = cell2mat(col(j));
        inhibitory_nodes(ele) = setdiff(col, ele);
    end
end
activation_values = containers.Map;
keys_ = excitory_nodes.keys();
for i = 1:length(keys_)
    key = keys_{i};
    activation_values(key) = [-0.1];
end
new_val = zeros(1, 41);
probe_ = containers.Map(excitory_nodes.keys, new_val);
prompt = "What do you want to probe on?";
dlgtitle = "Probe Input";
dims = [1, 50];
answer = inputdlg(prompt, dlgtitle, dims);
answer = split(cell2mat(answer));
for i = 1:length(answer)
    value = cell2mat(answer(i));
    probe_(value) = 0.2;
end

% Set the number of iterations for the simulation
time = 200;

% Iterate through each time step
for i = 2:time
    for j = 1:length(keys_)
        node = keys_{j};
        % Extract the activation value for the current node at the previous time step
        val_list = activation_values(node);
        current_val = val_list(i-1);
        % retrieve the input value and the list of excitory nodes for the current node
        input_ = probe_(node);
        exc_nodes = excitory_nodes(node);
        % retrieve the activation value for excitory node at current
        % and previous time step and increase weight of activation value by 5 percent
        for k = 1:length(exc_nodes)
            exc_node = exc_nodes{k};
            excval_list = activation_values(exc_node);
            excval = excval_list(i-1);
            input_ = input_ + 0.05*excval;
        end
        
        % retrieve list of inhibitory nodes connected to current node
        inhb_nodes = inhibitory_nodes(node);
        % retrieve activation value for inhibitory node at current and
        % previous time step and decreases weight of activation value by 3 percent
        for k = 1:length(inhb_nodes)
            inhb_node = inhb_nodes{k};
            inhbval_list = activation_values(inhb_node);
            inhbval = inhbval_list(i-1);
            input_ = input_ - 0.03*inhbval;
        end
        
        % for positive input values calculate excitatory effect
        if (input_ > 0)
            effect_ = (1-current_val)*input_;
        % for non-positive values calculate inhibitory effect
        else
            effect_ = (current_val+0.2)*input_;
        end
        % calculate and update list of activation values for current node
        new_val = current_val + effect_ - 0.05*(current_val-0.1);
        activation_values(node) = [activation_values(node), new_val];
    end
end

% for each column retrieve unique elements
for i = 1:6
    col = unique(table2array(js_data(:, i)));
    % create new variable to store maximum activation value in each column
    maxi_ = 0;
    % iterates through each element in each column until max value of maxi_ is determined
    for j = 1:size(col, 1)
        ele = cell2mat(col(j));
        actval_list = activation_values(ele);
        act_val = actval_list(200);
        if(act_val>maxi_)
            maxi_ = act_val;
            max_col = ele;
        end
    end
    % display maximum activation values for current column
    disp(max_col)
    disp(maxi_)
end
