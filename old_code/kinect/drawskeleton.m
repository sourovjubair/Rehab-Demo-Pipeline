function drawskeleton(data,gfx,l)
n = size(l,2);
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

for i = 1:n
    X1 = [data(SkeletonConnectionMap(l(i),1),1) data(SkeletonConnectionMap(l(i),2),1)];
    Y1 = [data(SkeletonConnectionMap(l(i),1),2) data(SkeletonConnectionMap(l(i),2),2)];
    gfx(i).XData = X1;
    gfx(i).YData = Y1;
end

end