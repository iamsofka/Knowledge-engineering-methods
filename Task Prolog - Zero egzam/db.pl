:- dynamic my_room/1.
:- dynamic items_in_room/2.

my_room(kitchen).

pass(kitchen, corridor).
pass(bedroom, corridor).
pass(bathroom, corridor).

pass(corridor, kitchen) :-
	pass(kitchen, corridor).

pass(corridor, bedroom) :-
	pass(bedroom, corridor).

pass(corridor, bathroom) :-
	pass(bathroom, corridor).

item(teapot).
item(lamp).
item(bottle).

room(kitchen).
room(corridor).
room(bathroom).
room(bedroom).

items_in_room(kitchen, []).
items_in_room(corridor, []).
items_in_room(bathroom, []).
items_in_room(bedroom, []).


add_item_to_room(X, C) :-
	not(room(X)),
	format('There is no such room (~w)', [X]),!.

add_item_to_room(X, C) :-
	not(item(C)),
	format('There is no such item (~w)', [C]),!.

add_item_to_room(X, C) :-
	my_room(Z),
	not(X = Z),
	format('You cannot put ~w ', [C]),
	format('into ~w ', [X]),
	format('because you are in ~w ', [Z]),!.

add_item_to_room(X, C) :-
	item(C),
	room(X),
	items_in_room(X, Y),
	append(Y, [C], Z),
	retractall(items_in_room(X, _)),
	assert(items_in_room(X, Z)),
	format('Added ~w ', [C]),
	format('to ~w ', [X]), nl,
	format('Items: ~w ', [Z]),
	format('in ~w ', [X]).

remove_item_from_room(X, C) :-
	item(C),
	room(X),
	items_in_room(X,Y),
	delete(Y,C,Z),
	retractall(items_in_room(X, _)),
	assert(items_in_room(X, Z)),
	format('Removed ~w ', [C]),
	format('from ~w ', [X]).

go_to_room(Y) :-
	not(room(Y)),
	format('There is no such room (~w)', Y),!.

go_to_room(Y) :-
	my_room(X),
	Y = X,
	format('You are already in ~w', [Y]),!.

go_to_room(Y) :-
	my_room(X),
	not(pass(X, Y)),
	format('~w ', [Y]),
	format('has no pass to ~w', [X]),!.

go_to_room(Y) :-
	my_room(X),
	pass(X,Y),
	retract(my_room(X)),
	assert(my_room(Y)),
	format('You are in ~w', [Y]).


current_room :-
	my_room(X),
	format('You are in ~w', [X]).

get_items_in_room(X) :-
	items_in_room(X,Y),
	format('Items: ~w ', [Y]),
	format('in ~w ', [X]).



/*

current_room.
go_to_room(sdafasdf).
go_to_room(bathroom).
go_to_room(kitchen).
go_to_room(corridor).
add_item_to_room(asdf, asdf).
add_item_to_room(kitchen, asdf).
add_item_to_room(kitchen, lamp).
add_item_to_room(corridor, lamp).
get_items_in_room(corridor).
add_item_to_room(corridor, bottle).
get_items_in_room(corridor).
remove_item_from_room(corridor, bottle).
get_items_in_room(corridor).

*/