function trackbody = gettrackidx(meta)
if sum(meta.IsBodyTracked)==0
    trackbody = 0;
else
    trackbody = find(meta.IsBodyTracked,1);
    trackbody = trackbody(1);
end
end