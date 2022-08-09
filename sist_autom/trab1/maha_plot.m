function maha_plot(els,ns)
n = size(els, 2)/2;

%figure
hold on

for i = 1:n
    plot(els(:,2*i-1),els(:,2*i),'LineWidth',2)
end
%legend(arrayfun(@(mode) sprintf('%d Sigma', mode), ns, 'UniformOutput', false));
end