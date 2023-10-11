% Your 2D arrays:
x1 = [1 2; 3 4];
x2 = [2 3; 4 5];
% Concatenate:
x = cat(3,x1,x2);
% Permute to get interpolated dimension first:
x = permute(x,[3 1 2])
% Define arbitrary unit for time slices:
t0 = [1 2];
% Interpolate to time slice at t=1.5:
x_interp = interp1(t0,x,1.5)

##X = [1:3]';
##Y1 = [1:3]';
##Y2 = [4:6]';
##XI = [1.5:2.5]';
##
##X = repmat(X, 1, 2);
##Y = cat(2, Y1, Y2);
##XI = repmat(XI, 1, 2);
##
##interp1(X(:,1), Y(:,1), XI(:,1))
##interp1(X(:,2), Y(:,2), XI(:,2))

##[XX, YY] = meshgrid(1:3,1:3);
##
##ZZ = XX.*YY;
##
##[XXI, YYI] = meshgrid(1.5:2.5, 1.5:2.5);
##
##Z = repmat(Z, 1, 1, 2);
##XI = repmat(XI, 1, 1, 2);
##YI = repmat(YI, 1, 1, 2);