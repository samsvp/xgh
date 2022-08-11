function p = prob_normal(a, bsquared)
    p = (1 / sqrt(2 * pi * bsquared)) * exp(-0.5 * a^2/bsquared);
end