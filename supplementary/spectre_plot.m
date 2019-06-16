clear all; 
close all;

% Génération de la série d'impulsions
Fe  = 44000;
duree = 1.;                    % en secondes
taille = Fe*duree;
n = Fe/2;
f0 = 200;                      % on veut f0 impulsions par seconde -> f0*duree dans le vecteur -> une tous les taille/f0 echantillons
t = (0:n-1)/Fe;                % vecteur temps

nb_imp = f0*duree;
pas = floor(taille/nb_imp);
clics = zeros(1,taille);
for i = 0:(nb_imp-2)
    clics((i*pas)+1) = 1;    
end

% Filtrage
f_bump = f0*15;                       % modifie it to move the spectral bump
Wo = f_bump/(Fe/2);
Q = 30;
[B,A] = nt_filter_peak2(Wo,Q);
son = filter(B,A,clics);

% Calcul du spectre
n = length(son);
z = fft(son);                         % FFT
% normalisation
zmax = max(abs(z));
sp =abs(z(1:n/2))/zmax;
sp_db = 20*log(sp);
    
% tracé du spectre
scrsz = get(0,'ScreenSize');
figure('Position',[scrsz(3)/4 scrsz(4)/4 scrsz(3)/2 scrsz(4)/2],'NumberTitle','off','Name','Spectre du signal','Color','White');
fmin = 1;                              % choix de la plage d'affichage
fmax = 4000;
f = (0:n/2-1)*Fe/n;
subplot(2,1,1); plot(f, sp); xlabel('frequence (Hz)'); ylabel('Amplitude'); title('Spectre');axis([fmin fmax 0 1]);              
subplot(2,1,2); plot(f, sp_db); xlabel('frequence (Hz)'); ylabel('Amplitude'); title('Spectre db');axis([fmin fmax -50 0]);
