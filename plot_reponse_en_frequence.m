clear all;
close all;

% Parametres
Fe = 40000;
f0 = 200;
f_bump = 7*f0;
Wo = f_bump/(Fe/2);
Q = 30;
BW=Wo/Q;

BW = BW*pi; % frequencies are normalized by pi.
Wo = Wo*pi; % frequencies are normalized by pi.

% Compute transfer function
gain = 1/(1+tan(BW/2));
B  = (1-gain)*[1 0 -1];              % numérateur
A  = [1 -2*gain*cos(Wo) (2*gain-1)]; % dénominateur

[h,w] = freqz(B,A, 512, Fe);
h_max = max(abs(h));
n = length(h);
h = abs(h)/h_max;
h_db = 20*log(h);

% Plot
figure;
plot(w,h_db);
xlabel('fréquences (Hz)', 'FontSize',13);
ylabel("Attenuation", 'FontSize',13);
title("Réponse impultionnelle du filtre résonnant", 'FontSize',15);
ylim([-50 0]);