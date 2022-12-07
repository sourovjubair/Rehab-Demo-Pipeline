colorVid = videoinput('kinect',1);
depthVid = videoinput('kinect',2);
vids = [colorVid depthVid];
src = getselectedsource(depthVid);
src.EnableBodyTracking = 'on';
colorVid.FramesPerTrigger = inf;
depthVid.FramesPerTrigger = inf;

screen = [1080,1920];
screen = screen/4;
fig = figure('Visible','off','Position',[1920-screen(2),1080-screen(1)-50,screen(2),screen(1)]);
ha = axes('Units','pixels','Position',[0,0,screen(2),screen(1)]);
frame = zeros(screen(1),screen(2),3,'uint8');
gImg = imshow(frame,'Parent', ha);
fig.Visible = 'on';

gLines = gobjects(24,1);
for i = 1:24
    gLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', 'o', 'Color', 'g');
end

% imwrite(getsnapshot(colorVid),'color.png');
% imwrite(getsnapshot(depthVid),'depth.png');

start(vids);
while depthVid.FramesAvailable<1
    pause(.1);
end

run = 10;
for i=1:run
    
%     tic;
%     [~,~,meta] = getdata(depthVid,1);
%     toc
    
    tic;
    [cframe,~] = getdata(colorVid,1);
    toc
%     
%     tic;
%     t = gettrackidx(meta);    
%     if t>0
%     jidx = meta.ColorJointIndices(:,:,t)*0.5333;
%     drawskeleton(jidx,gLines,1:24);
%     end
%     toc
%     
    tic;
    cframe = imresize(cframe, 1/4);
    gImg.CData = cframe;
    toc
    
    tic;
    drawnow
    toc
    disp('---');
end

stop(vids);
delete(vids);