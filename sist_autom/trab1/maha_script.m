m = [5;5]; % Média
S = [1 0.5;0.5 1]; % Variância
ns = [1;2;3]; % Normas de Maha

elps = [];

for i = 1:length(ns)
    elps = [elps, maha(m,S,ns(i))];
end

maha_plot(elps,ns);