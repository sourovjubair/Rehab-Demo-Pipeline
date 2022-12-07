clearvars
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

keepRunning = 1;
global record;
record = 0;
foundOnce = 0;

%GUI Creation
%  Create and then hide the UI as it is being constructed.
fig = figure('Visible','off','Position',[300,300,600,424]);

%  Construct the components.
hstart = uicontrol('Style','pushbutton','String','Start',...
       'Position',[520,424/2+25,70,25],...
       'Callback',@(src,evnt)buttonCallback(1));
hstop = uicontrol('Style','pushbutton','String','Stop',...
       'Position',[520,424/2-25,70,25],...
       'Callback',@(src,evnt)buttonCallback(0));
ha = axes('Units','pixels','Position',[0,0,512,424]);

align([hstart,hstop],'Center','None');

% Make the UI visible.
fig.Visible = 'on';
%gui

gImg = imshow(zeros(424,512,'uint16'));
gLines = gobjects(24,1);
for i = 1:24
    gLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'b');
end

start(vid);
while vid.FramesAvailable<fLimit
    pause(.1);
end

dataCount = 0;
while keepRunning
    [frames,~,meta] = getdata(vid,fLimit);
    % loop thru frames
    f = 1;
    thisMeta = meta(f);
    gImg.CData = frames(:,:,:,f);

    % on body track
    if(any(thisMeta.IsBodyTracked))            
        foundOnce = 1;
        trackbody = find(thisMeta.IsBodyTracked);
        trackbody = trackbody(1);
        if record
%             disp('recording');
            data(dataCount+1) = thisMeta;
            dataCount = dataCount + 1;
        else
            if dataCount>0
                %save data
                save("data/"+datestr(datetime('now'),"yyyy-mm-dd-HH-MM-SS")+".mat",'data');
                dataCount = 0;
                clear data
            end
        end
        % get 2d coordinates
        jointIndices = thisMeta.DepthJointIndices(:, :, trackbody);
%         disp(thisMeta.JointPositions(1, :, trackbody));
        for i = 1:8%24
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

%gui callbacks
function buttonCallback(data) 
% Display surf plot of the currently selected data.
% disp("click!");
global record;
record = data;
end
    