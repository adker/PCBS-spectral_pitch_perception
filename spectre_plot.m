    function spectre_ad(son, Fe, fmax) 
    n = length(son);
    z = fft(son);                         % FFT
    % normalisation
    zmax = max(abs(z));
    sp =abs(z(1:n/2))/zmax;
    sp_db = 20*log(sp);
    
    % tracé
    scrsz = get(0,'ScreenSize');
    figure('Position',[scrsz(3)/4 scrsz(4)/4 scrsz(3)/2 scrsz(4)/2],'NumberTitle','off','Name','Spectre du signal','Color','White');
    fmin = 1;                     % choix de la plage d'affichage
    %fmax = Fe/2;
    f = (0:n/2-1)*Fe/n;
    subplot(2,1,1); plot(f, sp); xlabel('frequence (Hz)'); ylabel('Amplitude'); title('Spectre');axis([fmin fmax 0 1]);              
    subplot(2,1,2); plot(f, sp_db); xlabel('frequence (Hz)'); ylabel('Amplitude'); title('Spectre db');axis([fmin fmax -50 0]);
end