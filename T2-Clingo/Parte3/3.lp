amistad(juan,maria).
amistad(maria,elena).
amistad(elena,fernando).
amistad(fernando,juan).
% amistad(maria,elena).
% amistad(maria,fernando).
% amistad(elena,pedro).
% amistad(elena,andres).

amistad(X,Y) :- amistad(Y,X).

usuario(X) :- amistad(X,Y).
usuario(Y) :- amistad(X,Y).

visible(maria).

% amistad visible
amistad_visible(X,Y) :- amistad(X,Y), visible(X).
amistad_visible(X,Y) :- amistad(X,Y), visible(Y).

% conectados por n
% caso base
conectados_por_n(X,Y,0) :- amistad_visible(X,Y).
conectados_por_n(X,Y,1) :- not amistad_visible(X,Y), amistad(X,Y).

% caso inductivo
conectados_por_n(X,Y,N) :- conectados_por_n(X,Z,N1), conectados_por_n(Z,Y,N2), N=N1+N2, X!=Y, #count{A,B : amistad(A,B), not amistad_visible(A,B)} >= N*2.

% cadena minima n
cadena_minima_n(X,Y,N) :- conectados_por_n(X,Y,N), N = #min{N1 : conectados_por_n(X,Y,N1)}.

