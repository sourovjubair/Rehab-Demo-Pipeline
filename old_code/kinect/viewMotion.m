load 'OR3.mat'
data1 = data;
load 'OR4.mat'
data2 = data;

%  Create and then hide the UI as it is being constructed.
f = figure('Visible','off','Position',[300,300,1024,424]);
ha = axes('Units','pixels','Position',[0,0,512,424]);
imshow(zeros(424,512,'uint16'));
ha1 = axes('Units','pixels','Position',[513,0,512,424]);
imshow(zeros(424,512,'uint16'));

% Make the UI visible.
f.Visible = 'on';

SkeletonConnectionMap = [ [4 3];  % Neck
                          [3 21]; % Head
                          [21 2]; % Right Leg
                          [2 1];
                          [21 9];
                          [9 10];  % Hip
                          [10 11];
                          [11 12]; % Left Leg
                          [12 24];
                          [12 25];
                          [21 5];  % Spine
                          [5 6];
                          [6 7];   % Left Hand
                          [7 8];
                          [8 22];
                          [8 23];
                          [1 17];
                          [17 18];
                          [18 19];  % Right Hand
                          [19 20];
                          [1 13];
                          [13 14];
                          [14 15];
                          [15 16];
                        ];



gLines = gobjects(24,1);
for i = 1:24
    gLines(i) = line(ha,[0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'b');
end

gLines1 = gobjects(24,1);
for i = 1:24
    gLines1(i) = line(ha1,[0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'b');
end

size1 = size(data1,2);
size2 = size(data2,2);
for f = 1:max([size1,size2])
%     disp(f);
    if(f<=size1)
        trackbody = find(data1(f).IsBodyTracked);
        trackbody = trackbody(1);
        jointIndices = data1(f).DepthJointIndices(:, :, trackbody);
        for i = 1:24
            X1 = [jointIndices(SkeletonConnectionMap(i,1),1) jointIndices(SkeletonConnectionMap(i,2),1)];
            Y1 = [jointIndices(SkeletonConnectionMap(i,1),2) jointIndices(SkeletonConnectionMap(i,2),2)];
            gLines(i).XData = X1;
            gLines(i).YData = Y1;
        end
    end
    if(f<=size2)
        trackbody = find(data2(f).IsBodyTracked);
        trackbody = trackbody(1);
        jointIndices = data2(f).DepthJointIndices(:, :, trackbody);
        for i = 1:24
            X1 = [jointIndices(SkeletonConnectionMap(i,1),1) jointIndices(SkeletonConnectionMap(i,2),1)];
            Y1 = [jointIndices(SkeletonConnectionMap(i,1),2) jointIndices(SkeletonConnectionMap(i,2),2)];
            gLines1(i).XData = X1;
            gLines1(i).YData = Y1;
        end
    end
    drawnow
end