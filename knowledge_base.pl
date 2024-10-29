%England
country(cruiserII, england).

light(cruiserII).       %1
medium(cruiserIII).     %2
medium(cruiserIV).      %3
heavy(matilda).         %4
heavy(churchill).       %5
heavy(blackPrince).     %6 
heavy(caernarvon).      %7
heavy(conquerror).      %8
heavy(fv215b).          %9

%France
country(r35, france).

medium(r35).        %1
medium(amx38).      %2
heavy(d2).          %3
heavy(b1).          %4
light(amx12t).      %5
light(amx1375).     %6
light(amx1390).     %7
light(bc25tAP).     %8
light(bc25t).       %9


%Branch. You can upgrade T1 to get T2
upgrade(cruiserII, cruiserIII, fact).
upgrade(cruiserIII, cruiserIV, fact).
upgrade(cruiserIV, matilda, fact).
upgrade(matilda, churchill, fact).
upgrade(churchill, blackPrince, fact).
upgrade(blackPrince, caernarvon, fact).
upgrade(caernarvon, conquerror, fact).
upgrade(conquerror, fv215b, fact).
upgrade(r35, amx38, fact).
upgrade(amx38, d2, fact).
upgrade(d2, b1, fact).
upgrade(b1, amx12t, fact).
upgrade(amx12t, amx1375, fact).
upgrade(amx1375, amx1390, fact).
upgrade(amx1390, bc25tAP, fact).
upgrade(bc25tAP, bc25t, fact).



level(cruiserII, 1).
level(r35, 1).

%transitivity of upgrade option
upgrade(T1, T2, rule) :- upgrade(T1, T3, fact), upgrade(T3, T2, _).

%All tanks in one branch are from the same country
country(T1, C) :- upgrade(T2, T1, _) , country(T2, C).

%get tank level
level(T, Lvl) :-
    upgrade(PrevT, T, fact),
    level(PrevT, N),
    Lvl is N + 1.


%T2 and T1 same type tanks, but T2 level is higher
same_type_higher_level(T1, T2) :-
    level(T1, Lvl1), level(T2, Lvl2), (
	(heavy(T1), heavy(T2), Lvl2 > Lvl1);
	(medium(T1), medium(T2), Lvl2 > Lvl1);
	(light(T1), light(T2), Lvl2 > Lvl1)).

%T2 is more protected than T1
protected(T1, T2) :- 
    same_type_higher_level(T1, T2) ;
    (heavy(T2), medium(T1)) ;
    (heavy(T2), light(T1)) ;
    (medium(T2), light(T1)).

%T2 is faster than T1
faster(T1, T2) :- 
    same_type_higher_level(T1, T2) ;
    (medium(T2), heavy(T1)) ;
    (light(T2), heavy(T1)) ;
    (light(T2), medium(T1)).
