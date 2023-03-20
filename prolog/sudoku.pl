:- use_module(library(clpfd)).


sudoku(Rows) :-
    % sanity checks
    length(Rows, 9),
    maplist(same_length(Rows), Rows), % check if all rows length are the same
    append(Rows, Vs), Vs ins 1..9, % check if all numbers are between 1 and 9
    % constraints
    transpose(Rows, Columns),
    maplist(all_distinct, Rows), % all rows must have different numbers
    maplist(all_distinct, Columns), % all columns must have different numbers
    Rows = [As, Bs, Cs, Ds, Es, Fs, Gs, Hs, Is],
    % all squares must have different numbers
    squares(As, Bs, Cs),
    squares(Ds, Es, Fs),
    squares(Gs, Hs, Is).

squares([],[],[]).
squares([N1, N2, N3|Ns1],
        [N4, N5, N6|Ns2],
        [N7, N8, N9|Ns3]) :-
            all_distinct([N1, N2, N3, N4, N5, N6, N7, N8, N9]),
            squares(Ns1, Ns2, Ns3).


main :-
    Rows = [
        [_, _, _, _, _, _, _, _, _],
        [_, _, _, _, _, 3, _, 8, 5],
        [_, _, 1, _, 2, _, _, _, _],
        [_, _, _, 5, _, 7, _, _, _],
        [_, _, 4, _, _, _, 1, _, _],
        [_, 9, _, _, _, _, _, _, _],
        [5, _, _, _, _, _, _, 7, 3],
        [_, _, 2, _, 1, _, _, _, _],
        [_, _, _, _, 4, _, _, _, 9]],
    sudoku(Rows), 
    maplist(label, Rows), 
    maplist(portray_clause, Rows).