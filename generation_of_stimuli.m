clear all; 
close all;

%path = 'C:\Users\adrie\Documents\Cours\Cogmaster\S2\Stage LSP\exp\generation_stim\stim\'
path = 'stimuli\'
%% Parametres generaux

Fe = 44100;

duree_son = 4;              % plus long que ce qu'on va pr�senter au sujet (pour pouvoir modifier la longeur si besoin)

Q = 100;                    % facteur de qualite du filtre
n = duree_son*Fe;
t = (0:n)/Fe;               % vecteur temps


%% G�n�ration des stimuli

fondamentales = [200, 220, 210, 230];

f_c = [7, 11, 15];          % partiels r�solus/peu r�solus/non-r�solus

Q = 100;
n = duree_son*Fe;
t = (0:n)/Fe;               % vecteur temps

son_final = [];

for fond = 1:length(fondamentales)  % f0         
    f0 = fondamentales(fond);
    delta = f0/4;
    decalages = [-2*delta, -2*delta, -delta, delta]; % du fois -2*delta car on y test deux hypoth�ses
    son_base = clics(f0, Fe, duree_son+1.); % +1 sec car on va retirer la p�riode transitoire
    
    for i = 1:2                     % ordre
        for j = 1:3                 % f_c
            for k = 1:4             % comparaison
                centroide = (f_c(j)*f0) +decalages(k);
                % on passe l'impulsion dans un filtre r�sonnateur
                son_filtre = filtre(son_base, Fe, centroide, Q);
                % on retire l'attaque du son
                son_filtre = son_filtre(floor(0.5*Fe):length(son_filtre)-floor(0.5*Fe));
                % on normalise par la rms
                rms_son = sqrt(mean((son_filtre.*son_filtre)));
                son_filtre = son_filtre/rms_son;
                
                % sin du pattern "escalier"
                if k == 1
                    sin_plat = sin(2*pi*(f_c(j)-1)*f0*t); % fr�quence de l'harmonique de rang pr�c�dant 
                else
                    sin_plat = sin(2*pi*f_c(j)*f0*t);
                end
                
                % sin du pattern "lin�aire"
                sin_lin = sin(2*pi*centroide*t);
                if i == 1
                    sin1 = sin_plat;
                    sin2 = sin_lin;
                else
                    sin1 = sin_lin;
                    sin2 = sin_plat;
                end

                titre_sin1 = string(path)+'comparaison'+'_'+string(k)+'_'+'fc'+'_'+string(j)+'_'+'ordre'+'_'+string(i)+'_'+'f0'+'_'+string(fond)+'_'+'sin1'+'.wav';
                %titre_sin1 = string([path,'decalage',string(k),'_','fc',string(j),'_','ordre',string(i),'_','f0',string(fond),'_','sin1','.wav']);
                titre_sin2 = string(path)+'comparaison'+'_'+string(k)+'_'+'fc'+'_'+string(j)+'_'+'ordre'+'_'+string(i)+'_'+'f0'+'_'+string(fond)+'_'+'sin2'+'.wav';
                %titre_sin2 = string([path,'decalage',string(k),'_','fc',string(j),'_','ordre',string(i),'_','f0',string(fond),'_','sin2','.wav']);
                titre_son = string(path)+'comparaison'+'_'+string(k)+'_'+'fc'+'_'+string(j)+'_'+'ordre'+'_'+string(i)+'_'+'f0'+'_'+string(fond)+'_'+'son'+'.wav';
                %titre_son = string([path,'decalage',string(k),'_','fc',string(j),'_','ordre',string(i),'_','f0',string(fond),'_','son','.wav']);
                audiowrite(titre_sin1, sin1, Fe);
                audiowrite(titre_sin2, sin2, Fe);
                audiowrite(titre_son, son_filtre, Fe);
                
            end
        end
    end
end

%% G�n�ration des deux exemples

f0 = 300;

f_c = 7;

son_base = clics(f0, Fe, duree_son+1.); % +1 sec car on va retirer la p�riode transitoire

son_final = [];

centroide = f_c*f0;
son_filtre = filtre(son_base, Fe, centroide, Q);
son_filtre = son_filtre(floor(0.5*Fe):length(son_filtre)-floor(0.5*Fe));
rms_son = sqrt(mean((son_filtre.*son_filtre)));
son_filtre = son_filtre/rms_son;

sin_lin = sin(2*pi*centroide*t);
sin_decale = sin(2*pi*(centroide+100)*t); % d�calage arbitraire pour avoir une fr�quence perceptiblement diff�rente
                    
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
    serie_imp((i*pas)+1) = 1;  % penser au ; !!!!!
end

end

function son_filtre = filtre(son, Fe, bump, Q)

Wo = bump/(Fe/2);
[B,A] = nt_filter_peak(Wo,Q);
clics_filtre = filter(B,A,son);
son_filtre = clics_filtre*(max(son)/max(clics_filtre));

end