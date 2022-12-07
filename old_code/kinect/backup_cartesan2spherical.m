load 'data/2018-11-25-10-22-47.mat'
n = size(data,2);

sph = cell(n,3);
upperright = [9,10,11]; %3 = neck.
ref = [3,9,10];
for i=1:n
    t = gettrackidx(data(i));
    for j=1:3
        v = data(i).JointPositions(upperright(j),:,t) - data(i).JointPositions(ref(j),:,t);
        [a,e,r] = cart2sph(v(1),v(2),v(3));
        sph{i,j} = [a,e,r];
    end
end

f = 2;
trimmed = sph;
for i=2:n
    t = gettrackidx(data(i));
    da = 0;
    for j=1:3
        dj = sph{i,j} - sph{i-1,j};
        djmax = max(dj(1:2));
        if djmax > da
            da = djmax;
        end
    end
    if da>=0.02
        for j=1:3
            trimmed{f,j} = sph{i,j};
        end
        f = f+1;
    end
end

for j=1:3
    trimmed{f,j} = sph{n,j};
end
f = f+1;

trimmed(f:n,:) = [];
save("data1/"+datestr(datetime('now'),"yyyy-mm-dd-HH-MM-SS")+".mat",'trimmed');

function trackbody = gettrackidx(meta)
trackbody = find(meta.IsBodyTracked);
trackbody = trackbody(1);
end