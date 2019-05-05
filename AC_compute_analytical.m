function [freq] = AC_compute_analytical(son, f0, Fe)

    T0 = 1/f0;
    lag = floor(f0/5);
    tau = (0:(ceil(T0*Fe)+lag))/Fe;
    a_c = zeros(1, length(tau));

    section_son = son(round(length(son)/2):round(length(son)));
    for i = 1:length(tau)
        section_courante = son(round(length(son)/2)-(tau(i)*Fe):round(length(son))-(tau(i)*Fe));
        num = sum(section_son.*section_courante);
        den = sqrt(sum(section_son.*section_son))*sqrt(sum(section_courante.*section_courante));
        a_c(i) = num/den;
    end
    
    [pics_ac,pos_ac] = findpeaks(a_c,tau); % recherche des pics
    freqs = (1./pos_ac); 
    freq = freqs(1);
    
end