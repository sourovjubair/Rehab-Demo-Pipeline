clearvars
load 'data/2018-12-08-23-18-44.mat'
n = size(data,2);

screen = cell(n,4);
depth = cell(n,4);
upperright = [9,10,11,12]; %21 = neck.
ref = [21,9,10,11];
jlim = 4;
for i=1:n
    t = gettrackidx(data(i));
    jidx = data(i).DepthJointIndices(:, :, t);
    jpos = data(i).JointPositions(:,:,t);
    for j=1:jlim
        v = jidx(upperright(j),:) - jidx(ref(j),:);
        [a,e,r] = cart2sph(v(1),v(2),0);
        screen{i,j} = [a,e,r];
        
        v = jpos(upperright(j),:) - jpos(ref(j),:);
        [a,e,r] = cart2sph(v(1),v(2),v(3));
        depth{i,j} = [a,e,r];
    end
end

% f = 2;
trim2d = screen;
trim3d = depth;
% for i=2:n
%     t = gettrackidx(data(i));
%     da = 0;
%     for j=1:jlim
%         dj = depth{i,j} - depth{i-1,j};
%         djmax = max(dj);
%         if djmax > da
%             da = djmax;
%         end
%     end
%     if da>=0.001
%         for j=1:3
%             trim2d{f,j} = screen{i,j};
%             trim3d{f,j} = depth{i,j};
%         end
%         f = f+1;
%     end
% end
% 
% for j=1:3
%     trim2d{f,j} = screen{n,j};
%     trim3d{f,j} = depth{n,j};
% end
% f = f+1;
% 
% trim2d(f:n,:) = [];
% trim3d(f:n,:) = [];
save("data1/"+datestr(datetime('now'),"yyyy-mm-dd-HH-MM-SS")+".mat",'trim2d','trim3d');

function trackbody = gettrackidx(meta)
trackbody = find(meta.IsBodyTracked);
trackbody = trackbody(1);
end