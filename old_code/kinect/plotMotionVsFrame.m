load 'data/2018-09-26-11-41-36.mat'
frameSize = size(data,2);
p = zeros(frameSize,2);
for f=1:frameSize
trackbody = find(data(f).IsBodyTracked);
trackbody = trackbody(1);
p(f,:) = data(f).DepthJointIndices(11, :, trackbody);
end
figure;
plot(1:frameSize,p(:,1),'x-')
hold on
plot(1:frameSize,p(:,2),'ro-')
hold off