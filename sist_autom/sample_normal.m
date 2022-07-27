function s = sample_normal(bsquared)
    b = sqrt(bsquared);
    s = mean(2 * b * rand([12, 1]) - b);
end