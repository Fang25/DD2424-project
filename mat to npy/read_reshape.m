
audPath = 'E:\try\keyboard\P\';        
audDir  = dir([audPath '*.wav']); 
le=length(audDir) 

for i = 1:le          
    [p,Fs] = audioread([audPath audDir(i).name]); 
   
   p=reshape(p,1,2*size(p,1));
   totlong=size(p,2)
   P(i,:)=[p,zeros(1,2*4635-totlong)];
end
save('Pp.mat','P')

