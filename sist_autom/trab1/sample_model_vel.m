function v = sample_model_vel(u, xt_minus1, dt, alpha)
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

    v_hat = v + sample_normal(alpha1 * v^2 + alpha2 * w^2);
    w_hat = w + sample_normal(alpha3 * v^2 + alpha4 * w^2);
    gamma_hat = sample_normal(alpha5 * v^2 + alpha6 * w^2);
    
    x = xt_minus1(1);
    y = xt_minus1(2);
    theta = xt_minus1(3);
    x_line = x - v_hat/w_hat * sin(theta) + v_hat/w_hat * sin(theta + w_hat * dt);
    y_line = y + v_hat/w_hat * cos(theta) - v_hat/w_hat * cos(theta + w_hat * dt);
    theta_line = theta + w_hat * dt + gamma_hat * dt;

    v = [x_line, y_line, theta_line];
end