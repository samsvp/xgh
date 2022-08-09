function xt = sample_model_odo(x_odo,x_odo_line, xt_minus1, alpha)
    
    % constants
    alpha1 = alpha(1);
    alpha2 = alpha(2);
    alpha3 = alpha(3);
    alpha4 = alpha(4);

    x_bar = x_odo(1);
    y_bar = x_odo(2);
    theta_bar = x_odo(3);
    
    x_line_bar = x_odo_line(1);
    y_line_bar = x_odo_line(2);
    theta_line_bar = x_odo_line(3);
    
    drot1 = atan2(y_line_bar - y_bar, x_line_bar - x_bar) - theta_bar;
    dtrans = sqrt((x_bar - x_line_bar)^2 + (y_bar - y_line_bar)^2);
    drot2 = theta_line_bar - theta_bar - drot1;

    drot1_hat = drot1 - sample_normal(alpha1 * drot1^2 + alpha2 * dtrans^2);
    dtrans_hat = dtrans - sample_normal(alpha3 * dtrans^2 + alpha4 * drot1^2 + alpha4 * drot2^2);
    drot2_hat = drot2 - sample_normal(alpha1 * drot1^2 + alpha2 * dtrans^2);
    
    x = xt_minus1(1);
    y = xt_minus1(2);
    theta = xt_minus1(3);
    
    x_line = x + dtrans_hat * cos(theta + drot1_hat) ;
    y_line = y + dtrans_hat * sin(theta + drot1_hat);
    theta_line = theta + drot1_hat + drot2_hat;

    xt = [x_line, y_line, theta_line];
end