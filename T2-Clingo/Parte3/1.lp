amistad(juan,maria).
amistad(maria,elena).
amistad(elena,fernando).
amistad(fernando,juan).

usuario(X) :- amistad(X,Y).
usuario(Y) :- amistad(X,Y).

cadena(X,Y,Largo) :- amistad(X,Y), Largo=1.
cadena(X,Y,Largo) :- cadena(X,Z,L1), cadena(Z,Y,L2), Largo=L1+L2, #count{A,B : amistad(A,B)} >= Largo, X!=Y.
