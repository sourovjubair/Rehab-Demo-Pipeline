% load 'data/2018-09-25-20-19-39.mat'
% load 'data/2018-09-25-20-19-55.mat'
% load 'data/2018-09-25-22-42-09.mat'
% load 'data/2018-09-26-11-30-37.mat'
load 'data/2018-09-26-11-41-36.mat'
figure;
imshow(zeros(424,512,'uint16'));
hold on;
for f = 1:size(data,2)-1
    trackbody = find(data(f).IsBodyTracked);
    trackbody = trackbody(1);
    jointIndices = data(f).DepthJointIndices(:, :, trackbody);
    jointIndices1 = data(f+1).DepthJointIndices(:, :, trackbody);
    for i=9:11
        X1 = [jointIndices(i,1) jointIndices1(i,1)];
        Y1 = [jointIndices(i,2) jointIndices1(i,2)];
        plot(X1,Y1,'r-');
    end
    drawnow
end
hold off;