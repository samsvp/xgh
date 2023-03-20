is_head(X, [X|_]).

list_member(X,[X|_]).
list_member(X,[_|TAIL]) :- list_member(X,TAIL).

main :- write('Hello World').