<<<<<<< HEAD
function [B,A] = nt_filter_peak2(Wo,Q)
%[B,A] = nt_filter_peak(Wo,Q) - second order resonator filter
%
% Wo: peak frequency (1 == nyquist)( = pi radian/sample ?)
% Q: quality factor
%
% NoiseTools

if nargin<2; error('!'); end  
if Wo>1; error('normalized centre frequency should be < 1'); end

BW=Wo/Q;

% frequencies are normalized by pi.
BW = BW*pi;
Wo = Wo*pi;

gain = 1/(1+tan(BW/2));
B  = (1-gain)*[1 0 -1];   % num�rateur
A  = [1 -2*gain*cos(Wo) (2*gain-1)]; % d�nominateur
 
if ~nargout       
    figure(100);
    freqz(B,A);   
    figure(101);
    plot([-10:100],filter(B,A,[zeros(10,1);1;zeros(100,1)]));
    xlabel('s / sr');
end

=======
function [B,A] = nt_filter_peak2(Wo,Q)
%[B,A] = nt_filter_peak(Wo,Q) - second order resonator filter
%
% Wo: peak frequency (1 == nyquist)( = pi radian/sample ?)
% Q: quality factor
%
% NoiseTools

if nargin<2; error('!'); end  
if Wo>1; error('normalized centre frequency should be < 1'); end

BW=Wo/Q;

% frequencies are normalized by pi.
BW = BW*pi;
Wo = Wo*pi;

gain = 1/(1+tan(BW/2));
B  = (1-gain)*[1 0 -1];   % num�rateur
A  = [1 -2*gain*cos(Wo) (2*gain-1)]; % d�nominateur
 
if ~nargout       
    figure(100);
    freqz(B,A);   
    figure(101);
    plot([-10:100],filter(B,A,[zeros(10,1);1;zeros(100,1)]));
    xlabel('s / sr');
end

>>>>>>> 3dda64f4f4c97b176a1e25d78be93826dd028427
   