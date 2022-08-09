function p = prob_triangular(a, bsquared)
    p = max([0,(1/(sqrt(6*bsquared))) - abs(a)/(6*bsquared)]);
end