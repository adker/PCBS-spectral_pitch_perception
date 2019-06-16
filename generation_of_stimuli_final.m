clear all; 
close all;

path = 'stimuli/'

%% Parametres generaux

Fe = 44100;

duree_son = 4;              % plus long que ce qu'on va presenter au sujet (pour pouvoir modifier la longueur si besoin)

Q = 100;                    % facteur de qualite du filtre
n = duree_son*Fe;
t = (0:n)/Fe;               % vecteur temps


%% Generation des stimuli

fondamentales = [200, 220, 210, 230];

f_c = [7, 11, 15];          % partiels resolus/peu resolus/non-resolus

son_final = [];

for fond = 1:length(fondamentales)  % f0         
    f0 = fondamentales(fond);
    delta = f0/4;
    decalages = [-2*delta, -2*delta, -delta, delta]; % du fois -2*delta car on y test deux hypotheses
    son_base = clics(f0, Fe, duree_son+1.); % +1 sec car on va retirer la periode transitoire
    
    for i = 1:2                     % ordre
        for j = 1:3                 % f_c
            for k = 1:4             % comparaison
                centroide = (f_c(j)*f0) +decalages(k);
                % on passe l'impulsion dans un filtre resonnateur
                son_filtre = filtre(son_base, Fe, centroide, Q);
                % on retire l'attaque du son
                son_filtre = son_filtre(floor(0.5*Fe):length(son_filtre)-floor(0.5*Fe));
                % on normalise par la rms
                rms_son = sqrt(mean((son_filtre.*son_filtre)));
                son_filtre = son_filtre/rms_son;
                
                % sin du pattern "escalier"
                if k == 1
                    sin_plat = sin(2*pi*(f_c(j)-1)*f0*t); % frequence de l'harmonique de rang precedant 
                else
                    sin_plat = sin(2*pi*f_c(j)*f0*t);
                end
                
                % sin du pattern "lineaire"
                sin_lin = sin(2*pi*centroide*t);
                if i == 1
                    sin1 = sin_plat;
                    sin2 = sin_lin;
                else
                    sin1 = sin_lin;
                    sin2 = sin_plat;
                end

                titre_sin1 = sprintf('%s/comparaison_%d_fc_%d_ordre_%d_f0_%d_sin1.wav', path, k, j, i, fond);
                titre_sin2 = sprintf('%s/comparaison_%d_fc_%d_ordre_%d_f0_%d_sin2.wav', path, k, j, i, fond);             
                titre_son = sprintf('%s/comparaison_%d_fc_%d_ordre_%d_f0_%d_son.wav', path, k, j, i, fond);
                
                audiowrite(titre_sin1, sin1, Fe);
                audiowrite(titre_sin2, sin2, Fe);
                audiowrite(titre_son, son_filtre, Fe);
                
            end
        end
    end
end

%% Generation des deux exemples

f0 = 300;

f_c = 7;

son_base = clics(f0, Fe, duree_son+1.); % +1 sec car on va retirer la periode transitoire

son_final = [];

centroide = f_c*f0;
son_filtre = filtre(son_base, Fe, centroide, Q);
son_filtre = son_filtre(floor(0.5*Fe):length(son_filtre)-floor(0.5*Fe));
rms_son = sqrt(mean((son_filtre.*son_filtre)));
son_filtre = son_filtre/rms_son;

sin_lin = sin(2*pi*centroide*t);
sin_decale = sin(2*pi*(centroide+100)*t); % decalage arbitraire pour avoir une frequence perceptiblement differente
                    
audiowrite([path,'son_example.wav'], son_filtre, Fe);
audiowrite([path,'sin_good_example.wav'], sin_lin, Fe);
audiowrite([path,'sin_bad_example.wav'], sin_decale, Fe);

%sound(bad_ex, Fe);

%% Fonctions 

function serie_imp = clics(f0, Fe, duree)

taille = Fe*duree;
nb_imp = f0*duree;
pas = floor(taille/nb_imp);
serie_imp = zeros(1,taille);

for i = 0:(nb_imp-2)
    serie_imp((i*pas)+1) = 1;
end

end

function son_filtre = filtre(son, Fe, bump, Q)

Wo = bump/(Fe/2);
[B,A] = nt_filter_peak(Wo,Q);
clics_filtre = filter(B,A,son);
son_filtre = clics_filtre*(max(son)/max(clics_filtre));

end