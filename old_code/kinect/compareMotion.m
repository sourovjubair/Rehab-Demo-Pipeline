fLimit = 1;

vid = videoinput('kinect', 2);
src = getselectedsource(vid);
src.EnableBodyTracking = 'on';

vid.FramesPerTrigger = inf;

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

load 'data/2018-11-25-10-22-47.mat'
dataframes = size(data,2);
distancedata = zeros(dataframes,3,10);
rep = 1;

keepRunning = 1;
foundOnce = 0;

%GUI Creation
fig = figure('Visible','off','Position',[300,300,512,424]);
ha = axes('Units','pixels','Position',[0,0,512,424]);
fig.Visible = 'on';



gImg = imshow(zeros(424,512,'uint16'));
gLines = gobjects(24,1);
for i = 1:24
    gLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'b');
end

p = 0;
pLines = gobjects(24,1);
for i = 1:24
    pLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', 'o', 'Color', 'g');
end

gText = text(5,10,'');
gText1 = text(5,20,'');
gText2 = text(300,10,'0/0');
gText2.Color = 'w';

start(vid);
while vid.FramesAvailable<fLimit
    pause(.1);
end

idx2match = 1;

while keepRunning
    [frames,~,meta] = getdata(vid,fLimit);
    % loop thru frames
    f = 1;
    thisMeta = meta(f);
    gImg.CData = frames(:,:,:,f);
    
    p = idx2match;
    if(p<dataframes)
        datatrackbody = find(data(p+1).IsBodyTracked);
        datatrackbody = datatrackbody(1);
        jointIndices = data(p+1).DepthJointIndices(:, :, datatrackbody);
        for i = 1:24
            X1 = [jointIndices(SkeletonConnectionMap(i,1),1) jointIndices(SkeletonConnectionMap(i,2),1)];
            Y1 = [jointIndices(SkeletonConnectionMap(i,1),2) jointIndices(SkeletonConnectionMap(i,2),2)];
            pLines(i).XData = X1;
            pLines(i).YData = Y1;
        end
    end
%     p = mod(p+1,dataframes);
    
    % on feed body track
    if(any(thisMeta.IsBodyTracked))
        foundOnce = 1;
        trackbody = find(thisMeta.IsBodyTracked);
        trackbody = trackbody(1);
        
        % get 2d coordinates
        jointIndices = thisMeta.DepthJointIndices(:, :, trackbody);
        
        if p<dataframes
            % facing check
            dz_shoulder = abs(thisMeta.JointPositions(9,3,trackbody)-thisMeta.JointPositions(5, 3, trackbody))...
                -abs(data(idx2match).JointPositions(9,3,datatrackbody)-data(idx2match).JointPositions(5, 3, datatrackbody));
            if dz_shoulder<0.05
                facing = 1;
                gText.String = "Facing: 1";
                gText.Color = 'g';
            else
                facing = 0;
                gText.String = "Facing: 0";
                gText.Color = 'r';
            end
            % position check
            dz_body = norm(thisMeta.JointPositions(2,:,trackbody)-data(idx2match).JointPositions(2, :, datatrackbody));
            if dz_body<0.05
                position = 1;
                gText1.String = "Position: 1";
                gText1.Color = 'g';
            else
                position = 0;
                gText1.String = "Position: 0";
                gText1.Color = 'r';
            end
            gText2.String = num2str(idx2match)+"/"+num2str(dataframes);
            distancerighthand = 0;
            if position && facing
                distancerighthand = norm(thisMeta.JointPositions(11,:,trackbody)-data(idx2match).JointPositions(11, :, datatrackbody));
                distancerightelbow = norm(thisMeta.JointPositions(12,:,trackbody)-data(idx2match).JointPositions(12, :, datatrackbody));
                distancerightshoulder = norm(thisMeta.JointPositions(12,:,trackbody)-data(idx2match).JointPositions(12, :, datatrackbody));
                distancerighthand1 = norm(thisMeta.DepthJointIndices(11,:,trackbody)-data(idx2match).DepthJointIndices(11, :, datatrackbody));
%                 distancerightelbow = norm(thisMeta.DepthJointIndices(12,:,trackbody)-data(idx2match).DepthJointIndices(12, :, datatrackbody));
%                 distancerightshoulder = norm(thisMeta.DepthJointIndices(12,:,trackbody)-data(idx2match).DepthJointIndices(12, :, datatrackbody));

%                 disp([distancerighthand, distancerightelbow, distancerightshoulder]);
                epsilon = .10;
                epsilon1 = 20;
                if(distancerighthand1 < epsilon1)
                    distancedata(idx2match,:,rep) = [distancerighthand, distancerightelbow, distancerightshoulder];
                    idx2match = idx2match + 1;
                    if(idx2match >= dataframes)
                        rep = rep+1;
                        idx2match = 1;
                        disp(rep);
                    end
                    
                end
            end
        end
        gText2.String = num2str(idx2match)+"/"+num2str(dataframes)+"|"...
            +num2str(distancerighthand);
        % draw feed body
        for i = 1:24
            X1 = [jointIndices(SkeletonConnectionMap(i,1),1) jointIndices(SkeletonConnectionMap(i,2),1)];
            Y1 = [jointIndices(SkeletonConnectionMap(i,1),2) jointIndices(SkeletonConnectionMap(i,2),2)];
            gLines(i).XData = X1;
            gLines(i).YData = Y1;
        end
    else
        if foundOnce
            disp("breaking");
            keepRunning = 0;
            break;
        end
    end
    %     drawnow
end
stop(vid);
delete(vid);
close(fig);
