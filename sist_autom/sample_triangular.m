function t = sample_triangular(bsquared)
    b = sqrt(bsquared);
    t = sqrt(6) / 2 * ((2 * b * rand() - b) + (2 * b * rand() - b));
end