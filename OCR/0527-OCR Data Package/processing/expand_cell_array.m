function [ out ] = expand_cell_array( in )
% Accepts a "nested" cell array
% Returns a justified 2-d array

    % Determine width
    COLS = max(cellfun('length', in));
    ROWS = rows(in);

    out = cell(ROWS, COLS);

    for r=[1:ROWS]
        out(r,:) = in{r};
    end
end

