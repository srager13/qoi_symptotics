clear all
close all
clc

dataraw = parsecsv('output_batch_ocr_compiled.csv');

SCALES = [1.0:-0.1:0.2];

% Strip header and expand nested cell array
data_2d = expand_cell_array(dataraw(2:end,:));

% Refactor 2D cell array into 3D
[r,c] = size(data_2d);
n = 9;
data_3d = permute(reshape(data_2d', [c, r/n, n]), [2,1,3]);

% Get average accuracy for each scale
avg_acc = zeros(1,size(SCALES));
dev_acc = zeros(1,size(SCALES));
for i=[1:length(SCALES)]
    iteration_data = data_3d(:,:,i);
    acc_vec = cellfun(@str2num, data_3d(:,6,i));
    avg_acc(i) = mean(acc_vec);
    dev_acc(i) = std(acc_vec);
end

%plot(SCALES, avg_acc)
errorbar(SCALES, avg_acc, dev_acc)
xlabel('Resize Scale')
ylabel('Average Accuracy')
ylim([0,100])
title({'Resize Scale vs Average Accuracy';'(error bars show standard deviation)'})



