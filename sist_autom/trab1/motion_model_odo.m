function p = motion_model_odo(x_hypo,x_hypo_line,x_odo,x_odo_line, alpha)
    
    % constants
    alpha1 = alpha(1);
    alpha2 = alpha(2);
    alpha3 = alpha(3);
    alpha4 = alpha(4);
    
    % hypotheses
    x = x_hypo(1);
    y = x_hypo(2);
    theta = x_hypo(3);
    
    x_line = x_hypo_line(1);
    y_line = x_hypo_line(2);
    theta_line = x_hypo_line(3);
    
    % odometry
    x_bar = x_odo(1);
    y_bar = x_odo(2);
    theta_bar = x_odo(3);
    
    x_line_bar = x_odo_line(1);
    y_line_bar = x_odo_line(2);
    theta_line_bar = x_odo_line(3);
    
    
    drot1 = atan2(y_line_bar - y_bar, x_line_bar - x_bar) - theta_bar;
    dtrans = sqrt((x_bar - x_line_bar)^2 + (y_bar - y_line_bar)^2);
    drot2 = theta_line_bar - theta_bar - drot1;
    
    
    drot1_hat = atan2(y_line - y, x_line - x) - theta;
    dtrans_hat = sqrt((x - x_line)^2 + (y - y_line)^2);
    drot2_hat = theta_line - theta - drot1_hat;
    
    
    p = prob_normal(drot1 - drot1_hat, alpha1*drot1_hat^2 + alpha2*dtrans_hat^2) * ...
        prob_normal(dtrans - dtrans_hat, alpha3*dtrans_hat^2 + alpha4*drot1_hat^2 + + alpha4*drot2_hat^2) * ...
        prob_normal(drot2 - drot2_hat, alpha1*drot2_hat^2 + alpha2*dtrans_hat^2);
    

end
