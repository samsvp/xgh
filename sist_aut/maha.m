function elpt = maha(m, S, n)
    [PD,PV]=eig(S);
    PV=diag(PV).^.5;
    
    theta=linspace(0,2*pi,360)';
    elpt=n*[cos(theta),sin(theta)]*diag(PV)*PD' + m';
end