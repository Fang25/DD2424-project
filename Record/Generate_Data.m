CHUNK = 1024;
RATE = 44100;
% Read Wave-file
path = 'C:\Users\timce\Project_DD2424\Long\LONG_SEGMENT1.wav'
T = readtable('C:\Users\timce\Project_DD2424\Long\Key_ACTION1.csv');
%To save new wavefiles
PATH_FOLDER = 'C:\Users\timce\Project_DD2424\Created_Waves';
file_name = 'P';

%Length of created Audio
lb = 0.015;
ub = 0.09;
%%% Load the used characters 
key_chars = unique(T.Var2);
for i=1:length(key_chars)
    key_chars{i}
    mkdir(PATH_FOLDER, key_chars{i})
end

info = audioinfo(path);
[y, Fs] = audioread(path);

[num_keys, ~] = size(T.Var1);
num_tiks = round(info.Duration * 44100 / 1024);

t = 0:seconds(1/Fs):seconds(info.Duration);
t = t(1:end-1);
[~, L] = size(t);
n = 2^nextpow2(L);
Y = fft(y, n);
f = Fs*(0:(n/2))/n;
P = abs(Y/n);
figure;
plot(f, P(1:n/2+1))

figure;
plot(t, y)

t_tiks = info.Duration / num_tiks;

%Trying out Windowing 2 ms
w_s = 0.002;
F = [];
window = 0:seconds(w_s):seconds(info.Duration - w_s);
for i = 1:numel(window)
    t_i = linspace(seconds(window(i)),seconds(window(i))+w_s, 1103);
    y_ind = round(seconds(window(i)) * Fs):round((seconds(window(i))+w_s)*Fs);
    [~, L_i] = size(t_i);
    n_i = 2^nextpow2(L_i);
    %no_Sec = seconds(y_ind)
    Y_i = fft(y(y_ind(2:end)',1), n_i);
    f_i = Fs*(0:(n_i/2))/n_i;
    P = abs(Y_i/n_i);
    
    F = [F sum(P)];
end
figure;
plot(window, F)


% Here we find the peaks 
i = 5;
prev_max = 0;
threshold = 0.003;

over_threshold = 0;
is_key = 0;

save_wav = 1;
only_push = 1;
while(i < numel(F) - 100)
   [Ct, t] = max(F(i:i+5));
   t = i + t - 1;
   if Ct > threshold
       % Making sure that we are not at the beginning
       [Cq, q] = max(F(t+1:t+20));
       if Ct > Cq
           % Check if within range of key
           wr = 0;
           for q = 1:length(T.Var1)
               if checkrange(T.Var1(q), t_tiks, seconds(window(t)))
                   wr = 1;
                   is_key = is_key + 1;
                   
                   if save_wav
                       if only_push
                           if T.Var3{q} == 'P'P
                                create_wav(y,PATH_FOLDER,T.Var2{q}, seconds(window(t)),file_name, q, lb, ub);
                                 i = t + 100;
                           else
                               i = t + 10;
                           end
                           
                       else
                           create_wav(y,PATH_FOLDER,T.Var2{q}, seconds(window(t)),file_name, q, lb, ub);
                           i = t + round(ub/ w_s);
                       end
                   else
                       i = t + 10;
                   end
               
                   break;
               end
           end
           if wr==0
               i = t + 1;
           end
           over_threshold = over_threshold + 1;
           
       else
           i = q + i;
       end
    
   else
        i = t + 1;
   end

end
% p_f path to parent folder
% pn_f path path to new folder
% num
function create_wav(y, p_f, key, peak_time, file_name, num_file, lb, ub)
    disp(num_file)
    file_name =[p_f,  '\',key, '\', file_name, int2str(num_file) , '.wav']
    
    lower = round((peak_time - lb) * 44100)
    upper = round((peak_time + ub) * 44100)
    yt = zeros(length(y(lower:upper, 1)), 2);
    yt(:,1) = y(lower:upper, 1);
    yt(:,2) = y(lower:upper, 2);
    audiowrite(file_name, yt, 44100)

end
% Returns if within Range of a key, 
function b = checkrange(num_tiks, t_tiks, cur_time)
    key_down = 0.02;
    key_up   = 0.03;
    if ((num_tiks* t_tiks + key_up)>= cur_time) && ((num_tiks* t_tiks - key_down)<= cur_time)
        b = 1;
    else     
        b = 0;
    end
end

        


