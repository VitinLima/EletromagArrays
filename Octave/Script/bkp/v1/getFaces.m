TRIfaces = [TETR(:,[1 2 3]); TETR(:,[1 4 2]); TETR(:,[1 3 4]); TETR(:,[2 4 3])];
TRIcomp = TRI(:, [1 3 2]);
[~, IA] = intersect(TRIfaces, TRIcomp, 'rows');
TRIfaces(IA,:) = [];
[~, IA] = intersect(TRIfaces, TRIcomp(:, [2 3 1]), 'rows');
TRIfaces(IA,:) = [];
[~, IA] = intersect(TRIfaces, TRIcomp(:, [3 1 2]), 'rows');
TRIfaces(IA,:) = [];