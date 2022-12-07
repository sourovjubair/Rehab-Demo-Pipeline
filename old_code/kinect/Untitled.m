load 'data/2018-09-26-11-41-36.mat'
data1 = data;
% load 'data/2018-11-25-10-22-47.mat'
% data2 = data;
% figure;
% f = imshow(uint8(data(1).BodyIndexFrame));
% bLines = gobjects(24,1);
% for i = 1:24
%     bLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'b');
% end
% gLines = gobjects(24,1);
% for i = 1:24
%     gLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', 'o', 'Color', 'g');
% end
% 
% t1 = gettrackidx(data1(1));
% t2 = gettrackidx(data2(1));
% 
% jointIndices1 = data1(1).JointPositions(:, :, t1);
% jointIndices2 = data2(1).DepthJointIndices(:, :, t2);
% drawskeleton(jointIndices1,bLines);
% drawskeleton(jointIndices2,gLines);

imshow(ones(424,512));
t1 = gettrackidx(data1(1));
jidx = data1(1).DepthJointIndices(:, :, t1);
for i = 1:25
    t=text(jidx(i,1),jidx(i,2),num2str(i));
end