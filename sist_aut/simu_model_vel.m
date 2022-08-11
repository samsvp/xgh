n = 1000;
xi = [0,0,0];

alpha =[0.001,0.001,0.1,0.1,0.01,0.01];

u = [1.0,0];
dt = 1;

Dots = zeros(3,n);
Like = zeros(n,1);

if u(1) == 0
    for i = 1:n
        Dots(:,i) = sample_model_vel([0.1, u(1)], xi, dt, alpha);
        Like(i) = motion_model_vel(Dots(:,i), [0.1, u(1)], xi, dt, alpha);
    end
else
    for i = 1:n
        Dots(:,i) = sample_model_vel(u, xi, dt, alpha);
        Like(i) = motion_model_vel(Dots(:,i), u, xi, dt, alpha);
    end
end

Like = Like/max(Like);

Dots2D = Dots(1:2,:);
m = mean(Dots2D');
Dots_bar = Dots2D - m';
S = Dots_bar*Dots_bar'/n;

ns = [1;2;3]; % Normas de Maha

elps = [];

for i = 1:length(ns)
    elps = [elps, maha(m',S,ns(i))];
end

figure(1)
hold on
if u(1) == 0
    scatter(xi(1),xi(2),1000,'.b')
    scatter(Dots(1,:) - mean(Dots(1,:)),Dots(2,:) - mean(Dots(2,:)),[], [Like,zeros(n,2)], '.')
    %scatter(Dots(1,:),Dots(2,:),'.k')
    maha_plot(elps-mean(elps),ns);
else
    scatter(xi(1),xi(2),1000,'.b')
    scatter(Dots(1,:), Dots(2,:), [], [Like,zeros(n,2)], '.')
    %scatter(Dots(1,:),Dots(2,:),'.k')
    maha_plot(elps, ns);
end
legend("Posição Inicial")