function sph = getboneangle(bone,ref,cart)
n = size(bone,2);
sph = cell(n,1);
for j=1:n
    v = cart(bone(j),:) - cart(ref(j),:);
    [a,e,r] = cart2sph(v(1),v(2),0);
    sph{j} = [a,e,r];
end
end

