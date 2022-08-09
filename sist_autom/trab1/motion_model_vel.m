function p = motion_model_vel(xt, u, xt_minus1, dt, alpha)
    % constants
    alpha1 = alpha(1);
    alpha2 = alpha(2);
    alpha3 = alpha(3);
    alpha4 = alpha(4);
    alpha5 = alpha(5);
    alpha6 = alpha(6);

    % control signal
    v = u(1);
    w = u(2);

    % past state
    x = xt_minus1(1);
    y = xt_minus1(2);
    theta = xt_minus1(3);

    % current state
    x_line = xt(1);
    y_line = xt(2);
    theta_line = xt(3);

    mu = 0.5 * ((x-x_line)*cos(theta) + (y-y_line)*sin(theta)) / ...
        ((y-y_line)*cos(theta) - (x-x_line)*sin(theta));
    xstar = (x + x_line) / 2 + mu * (y - y_line);
    ystar = (y + y_line) / 2 + mu * (x_line - x);
    rstar = sqrt((x-xstar)^2 + (y-ystar)^2);
    dtheta = atan2(y_line - ystar, x_line - xstar) - atan2(y - ystar, x - xstar);
    
    v_hat = (dtheta / dt) * rstar;
    w_hat = dtheta / dt;
    gamma_hat = ((theta_line - theta) / dt) - w_hat;

    p = prob_normal(v - v_hat, alpha1*v^2 + alpha2*w^2) * ...
        prob_normal(w - w_hat, alpha3*v^2 + alpha4*w^2) * ...
        prob_normal(gamma_hat, alpha5*v^2 + alpha6*w^2);

%     p = prob_normal(v - v_hat, alpha1*v^2 + alpha2*w^2) * ...
%         prob_normal(w - w_hat, alpha3*v^2 + alpha4*w^2);
end