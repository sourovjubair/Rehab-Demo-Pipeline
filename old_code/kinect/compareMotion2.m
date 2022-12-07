clearvars
fLimit = 1;

vid = videoinput('kinect',2);
src = getselectedsource(vid);
src.EnableBodyTracking = 'on';

vid.FramesPerTrigger = inf;


%load 'data1/2018-12-08-23-19-56.mat'
load 'OR3.mat'
dataframes = size(trim2d,1);
matchdetails = zeros(dataframes,50);
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
    gLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', 'o', 'Color', 'g');
end
p = 0;
bLines = gobjects(24,1);
for i = 1:24
    bLines(i) = line([0,0],[0,0], 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'r');
end

% gText = text(5,10,'');
% gText1 = text(5,20,'');
% gText2 = text(300,10,'0/0');
% gText2.Color = 'w';

start(vid);
while vid.FramesAvailable<fLimit
    pause(.1);
end

p = 1;
upperright = [9,10,11,12]; %21 = neck.
ref = [21,9,10,11];
jtlim = 4;

while keepRunning
    [frames,~,meta] = getdata(vid,fLimit);
    % loop thru frames
    f = 1;
    thisMeta = meta(f);
     gImg.CData = frames;
%     gImg.CData = uint16(thisMeta.BodyIndexFrame);
    
    % on feed body track
    if(any(thisMeta.IsBodyTracked))
        foundOnce = 1;
        tidx = gettrackidx(thisMeta);
        
        % get 2d coordinates
        jidx = thisMeta.DepthJointIndices(:, :, tidx);
        
        % draw feed body
        drawskeleton(jidx,bLines,1:8);
        
        if(p<=dataframes)
            mimic = jidx;
            
            for jt=1:jtlim
                r =  norm( jidx(upperright(jt),:) - jidx(ref(jt),:));
                ang = trim2d{p,jt};
                [dx,dy,dz] = sph2cart(ang(1),ang(2),r);
                mimic(upperright(jt),:) = mimic(ref(jt),:) + [dx,dy];
            end
            drawskeleton(mimic,gLines,6:8);
            
            % compare
            dv = zeros(4,1);
            for jt=1:jtlim
                dv(jt) = norm(mimic(upperright(jt),:) -  jidx(upperright(jt),:));
            end
%             disp(dv);
            if max(dv) < 20 && p <= dataframes
                if p==1
                    ttaken = 0;
                    starttime = thisMeta.AbsTime;
                else
                    ttaken = datenum(thisMeta.AbsTime-starttime)*24*60*60;
                end
                    matchdetails(p,(rep-1)*5+1) = ttaken;
                for jt=1:4
                    matchdetails(p,(rep-1)*5+jt+1) = dv(jt);
                end
                p = p+1;
                if(p > dataframes)
                    p = 1;
                    rep = rep+1
                    if(rep>5)
                        keepRunning = 0;
                    end
                end
            end
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
% save2xl(matchdetails);
stop(vid);
delete(vid);
close(fig);

function save2xl(data)
    xlswrite("excel2/"+datestr(datetime('now'),"yyyy-mm-dd-HH-MM-SS"),data);
end