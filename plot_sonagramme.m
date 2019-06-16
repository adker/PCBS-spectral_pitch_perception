clear all; 
close all;

taille_ecran = get(0,'ScreenSize');    % détermination de la taille de l'écran


%% Lecture du son
fichier_audio = 'throat_singing_example';
[son,Fe] = audioread([fichier_audio,'.wav']);

% Redimentionnement:
debut = 0;                     % en secondes
fin = 11;
duree = fin-debut;
n_d = max(1,round(Fe*debut));  % échantillons de début et de fin
n_f = Fe*fin;
son = son(n_d:n_f,1).';        % redimensionnement en un vecteur horizontal
n = length(son);
T = (n-1)/Fe;


%% Sonagramme

% Parametres
nfft = 1024;                    % nombre d'échantillons sur lesquels est calculé chaque FFT               
n_window= nfft;                 % condition permettant de mettre une fenêtre de Hanning
noverlap = ceil(n_window/2);    % nombre d'échantillons qui sont repris dans la fenêtre suivante
S = spectrogram(son,n_window,noverlap,nfft,Fe,'yaxis');   % calcul du sonagramme

fmax = 9000;                    % Plage de frequences
fmin = 0;                       % Plage de frequences
S = 10*log10(abs(S));           % calcul du module en dB
Smax =max(max(S));
Smin =min(min(S));

% affichage du sonagramme
figure('Position',[taille_ecran(3)/4 taille_ecran(4)/4 taille_ecran(3)/2 taille_ecran(4)/2],'NumberTitle','off','Name','Sonagramme du signal','Color','White');
imagesc([0 T],[0 Fe/2],S,[Smin Smax]);  
colormap(jet);
xlabel('Temps (s)','FontName','Century Gothic','FontSize',16);          
ylabel('Fréquence (Hz)','FontName','Century Gothic','FontSize',16);
set(gca,'FontName','Century Gothic','FontSize',14);
axis([0 T fmin fmax]);
title("Sonagramme d'un chant 'diphonique'", 'Fontsize', 20)
axis xy;          
