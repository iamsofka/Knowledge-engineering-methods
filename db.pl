:- dynamic curr_room/1.
:- dynamic things_in_room/2.

curr_room(bedroom).

room(bedroom).
room(hall).
room(kitchen).

thing(bed).
thing(lamp).
thing(pills).
thing(phone).
thing(pen).
thing(blowdryer).
thing(knife).

things_in_room(bedroom, [lamp, bed]).
things_in_room(hall, [pen, phone]).
things_in_room(kitchen, [knife]).

connection(hall, bedroom).
connection(bedroom, hall).

connection(hall, kitchen).
connection(kitchen, hall).

connection(bedroom, hall).
connection(kitchen, hall).

current_room :-
	curr_room(A),
	format('~w', [A]).

add_thing(A, _) :-
	not(room(A)),
	format('Given room (~w) does not exist', [A]),!.

add_thing(_, B) :-
	not(thing(B)),
	format('Given thing (~w) does not exist', [B]),!.

add_thing(A, B) :-
	curr_room(D),
	not(A = D),
	format('Forbidden putting ~w, because you are not in ~w room', [B, A]),!.

add_thing(A, B) :-
	thing(B),
	room(A),
	things_in_room(A, C),
	append(C, [B], D),
	retractall(things_in_room(A, _)),
	assert(things_in_room(A, D)),
	format('Put ~w ', [B]).

remove_thing(A, B) :-
	thing(B),
	room(A),
	things_in_room(A,C),
	delete(C,B,D),
	retractall(things_in_room(A, _)),
	assert(things_in_room(A, D)),
	format('Removed ~w ', [B]).

go_into(C) :-
	not(room(C)),
	format('No given room (~w)', C),!.

go_into(C) :-
	curr_room(A),
	C = A,
	format('You are already in ~w', [C]),!.

go_into(C) :-
	curr_room(A),
	not(connection(A, C)),
	format('Forbidden, no such connection'),!.

go_into(C) :-
	curr_room(A),
	connection(A,C),
	retractall(curr_room(A)),
	assert(curr_room(C)),
	format('Now you are in ~w', [C]),!.

get_things(A) :-
	things_in_room(A,C),
	format('things ~w ', [C]).
