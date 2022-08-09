function s = sample_normal(bsquared)
    b = sqrt(bsquared);
    s = sum(2 * b * rand([12, 1]) - b)/2;
end