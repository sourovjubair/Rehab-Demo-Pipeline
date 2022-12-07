% Create color and depth kinect videoinput objects.
vid = videoinput('kinect', 2);
fps = 30;

% Look at the device-specific properties on the depth source device,
% which is the depth sensor on the Kinect V2.
% Set 'EnableBodyTracking' to on, so that the depth sensor will
% return body tracking metadata along with the depth frame.
src = getselectedsource(vid);
src.EnableBodyTracking = 'on';

vid.FramesPerTrigger = fps*3;
vid.TriggerRepeat = inf;

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

% Start the depth acquisition objects.
% This begins acquisition, but does not start logging of acquired data.
start(vid);
while vid.FramesAvailable<=0
    pause(.5);
end
foundOnce = 0;
count = 0;
while vid.FramesAvailable>=0
    disp(vid.FramesAvailable);
    [framedata,~,metadata] = getdata(vid,fps);
    lastframeMetadata = metadata(f90);
    lastframe = framedata(:,:,:,f90);
    imshow(lastframe);
    
    disp(lastframeMetadata.IsBodyTracked);
    if(any(lastframeMetadata.IsBodyTracked))
        disp("Body found");
        count = count + 1;
        if(count == 5)
            snapData = lastframeMetadata;
        end
        foundOnce = 1;
        trackbody = find(lastframeMetadata.IsBodyTracked);
        trackbody = trackbody(1);
        jointIndices = lastframeMetadata.DepthJointIndices(:, :, trackbody);
        for i = 1:24
            X1 = [jointIndices(SkeletonConnectionMap(i,1),1) jointIndices(SkeletonConnectionMap(i,2),1)];
            Y1 = [jointIndices(SkeletonConnectionMap(i,1),2) jointIndices(SkeletonConnectionMap(i,2),2)];
            line(X1,Y1, 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'b');
            
            hold on;
        end
        hold off;
    else
        disp("body not found");
        if foundOnce
            disp("breaking");
            break
        end
    end
end
stop(vid);
delete(vid);