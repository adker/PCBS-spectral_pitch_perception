<<<<<<< HEAD
clear all; 
close all;

path = 'C:\Users\adrie\Documents\Cours\Cogmaster\S2\Stage LSP\exp\generation_stim\stim\'

%% Génération de stimuli

f0 = 200;
Fe = 44100;

delta = f0/4;
decalages = [-2*delta, -delta, 0, delta, 2*delta];

f_c = [7, 11, 15]; % partiels résolus/peu résolus/non-résolus

duree_son = 0.5;
duree_intra_stim = 0.1;
duree_inter_stim = 0.3;

son_base = clics(f0, Fe, duree_son+1.); % +1 sec car on va retirer la période transitoire

Q = 100;
n = duree_son*Fe;
t = (0:n)/Fe;                % vecteur temps

son_final = [];

for rep = 1:2 % repetitions
    for i = 1:2 % ordre
        for j = 1:3 % f_c
            for k = 1:5
                centroide = (f_c(j)*f0) +decalages(k);
                son_filtre = filtre(son_base, Fe, centroide, Q);
                son_filtre = son_filtre(floor(0.5*Fe):length(son_filtre)-floor(0.5*Fe));
                [freq] = AC_compute_analytical(son_filtre, f0, Fe);
            %[pic, freq] = AC_deux_sections(son_filtre, f0, Fe, 0., 0.15, false);
            %sin_ac = sin(2*pi*freq(1)*t);
                sin_ac = sin(2*pi*freq*t);
            %sp = spectre_ad_2(son_filtre, Fe, 4000);
            %[M,I] = max(sp);
            %sin_sp = sin(2*pi*I*t);
                sin_lin = sin(2*pi*centroide*t);
                if i == 1
                    son_final = [sin_ac, zeros(1, Fe*duree_intra_stim), son_filtre, zeros(1, Fe*duree_inter_stim), sin_lin, zeros(1, Fe*duree_intra_stim), son_filtre];
                else
                    son_final = [sin_lin, zeros(1, Fe*duree_intra_stim), son_filtre, zeros(1, Fe*duree_inter_stim), sin_ac, zeros(1, Fe*duree_intra_stim), son_filtre];
                end
                titre = path+string(k)+'_'+string(j)+'_'+string(i)+'_'+string(rep)+'.wav';
                audiowrite(titre, son_final, Fe);
            end
        end
    end
end

%% Fonctions 

function serie_imp = clics(f0, Fe, duree)

taille = Fe*duree;
nb_imp = f0*duree;
pas = floor(taille/nb_imp);
serie_imp = zeros(1,taille);

for i = 0:(nb_imp-2)
    serie_imp((i*pas)+1) = 1;  % penser au ; !!!!!
end

end

function son_filtre = filtre(son, Fe, bump, Q)

Wo = bump/(Fe/2);
[B,A] = nt_filter_peak(Wo,Q);
clics_filtre = filter(B,A,son);
son_filtre = clics_filtre*(max(son)/max(clics_filtre));

end

function sp = spectre_ad_2(son, Fe, fmax) 
    n = length(son);
    z = fft(son);                         % FFT
    % normalisation des deux spectres
    zmax = max(abs(z));
    sp = abs(z(1:n/2))/zmax;
    sp_db = 20*log(sp);
=======
clear all; 
close all;

path = 'C:\Users\adrie\Documents\Cours\Cogmaster\S2\Stage LSP\exp\generation_stim\stim\'

%% Génération de stimuli

f0 = 200;
Fe = 40000;

delta = f0/4;
decalages = [-2*delta, -delta, 0, delta, 2*delta];

f_c = [7, 11, 15]; % partiels résolus/peu résolus/non-résolus

duree_son = 0.5;
duree_intra_stim = 0.1;
duree_inter_stim = 0.3;

son_base = clics(f0, Fe, duree_son+1.); % +1 sec car on va retirer la période transitoire

Q = 100;
n = duree_son*Fe;
t = (0:n)/Fe;                % vecteur temps

son_final = [];

for rep = 1:2 % repetitions
    for i = 1:2 % ordre
        for j = 1:3 % f_c
            for k = 1:5
                centroide = (f_c(j)*f0) +decalages(k);
                son_filtre = filtre(son_base, Fe, centroide, Q);
                son_filtre = son_filtre(floor(0.5*Fe):length(son_filtre)-floor(0.5*Fe));
                [freq] = AC_compute_analytical(son_filtre, f0, Fe);
            %[pic, freq] = AC_deux_sections(son_filtre, f0, Fe, 0., 0.15, false);
            %sin_ac = sin(2*pi*freq(1)*t);
                sin_ac = sin(2*pi*freq*t);
            %sp = spectre_ad_2(son_filtre, Fe, 4000);
            %[M,I] = max(sp);
            %sin_sp = sin(2*pi*I*t);
                sin_lin = sin(2*pi*centroide*t);
                if i == 1
                    son_final = [sin_ac, zeros(1, Fe*duree_intra_stim), son_filtre, zeros(1, Fe*duree_inter_stim), sin_lin, zeros(1, Fe*duree_intra_stim), son_filtre];
                else
                    son_final = [sin_lin, zeros(1, Fe*duree_intra_stim), son_filtre, zeros(1, Fe*duree_inter_stim), sin_ac, zeros(1, Fe*duree_intra_stim), son_filtre];
                end
                titre = path+string(k)+'_'+string(j)+'_'+string(i)+'_'+string(rep)+'.wav';
                audiowrite(titre, son_final, Fe);
            end
        end
    end
end

%% Fonctions 

function serie_imp = clics(f0, Fe, duree)

taille = Fe*duree;
nb_imp = f0*duree;
pas = floor(taille/nb_imp);
serie_imp = zeros(1,taille);

for i = 0:(nb_imp-2)
    serie_imp((i*pas)+1) = 1;  % penser au ; !!!!!
end

end

function son_filtre = filtre(son, Fe, bump, Q)

Wo = bump/(Fe/2);
[B,A] = nt_filter_peak(Wo,Q);
clics_filtre = filter(B,A,son);
son_filtre = clics_filtre*(max(son)/max(clics_filtre));

end

function sp = spectre_ad_2(son, Fe, fmax) 
    n = length(son);
    z = fft(son);                         % FFT
    % normalisation des deux spectres
    zmax = max(abs(z));
    sp = abs(z(1:n/2))/zmax;
    sp_db = 20*log(sp);
>>>>>>> 3dda64f4f4c97b176a1e25d78be93826dd028427
end