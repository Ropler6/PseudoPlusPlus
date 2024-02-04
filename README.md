# Documentatia programului "Pseudo++"
---

## Informatii generale

* Programul Pseudo++ este un compilator de la o sursa la alta. Acesta transforma pseudocod scris cu o sintaxa similara cu cea de BAC in cod C++ ce poate fi compilat si executat.



## Inceputul programului

* Utilizatorului i se dechide o fereastra de tip terminal in care programul primeste va cere ca data de intrare fisierul ce trebuie transformat in C++ (cu extensia .pc), (optional) numele fisierului de iesire si calea (PATH) catre acesta.
* Fisierul de iesire (cu numele prestabilit "main.cpp") va fi pus in directorul curent daca nu este aleasa o cale.



## Etapa de preprocesare

* Programul verifica codul scris in Pseudo++ caracter cu caracter si prelucreaza in mod specific cuvintele cheie sau operatorii, incadrand operatorii matematici intre spatii si adaugand ';' dupa cuvinte cheie ce marcheaza terminarea unei instructiuni logice.
* De asemenea, programul contorizeaza numarul de linii din datele de intrare.



## Etapa de procesare

* Programul reia codul linie cu linie, cu schimbarile ulterioare adaugate de preprocesor, si il transforma in cod valid C++.
* Acesta efectueaza diferite operatii pe cuvintele cheie si pe instructiunile logice prezente:

### Generalitati
* Toate functiile verifica respectarea sintaxei si semnaleaza erori la gasirea unor probleme. Acestea sunt: lipsa de paraneze, folosirea unui tip de date invalid, lipsa declararii variabilelor, prezenta ilegala sau lipsa operatorilor, a variabilelor sau a literalelor, prezenta unor cuvinte/simboluri necunoscute programului, etc.
*Nu sunt verificate erorile algebrice sau de logica matematica.
* In programul principal este apelata functia process_line care apeleaza la randul ei celelalte functii pentru a procesa diferitele tipuri de structuri si intoarce linia procesata.

* Citire: "citeste <variable> (<tip de date>)"
  * Functia process_user_input proceseaza linii care efectueaza operatii de citire a datelor de intrare de un anumit tip de date.

* Afisare: "scrie <variabile/literal>"
  * Functia process_user_output proceseaza linii care efectueaza operatii de afisare a datelor.

* Logica: "daca <conditii> atunci <instructiuni> stop"
  * Functia process_if_statement proceseaza linii care efectueaza operatii conditionale logice.

* Structura repetitiva cu test initial: "cat timp <conditii> executa <instructiuni> stop"
  * Functia process_while_structure proceseaza atat structurile de forma "cat timp <conditii> executa <instructiuni> stop", cat si partea finala a structurile de tipul " repeta <instructiuni> cat timp <conditie>". Aceasta determina tipul structurii repetitive dupa prezenta cuvantului cheie "executa" si proceseaza diferit linia.

* Structura repetitiva cu test initial: "repeta <instructiuni> pana cand | cat timp <conditii>"
  * Functia process_repeat_until proceseaza structurile repetitive cu test initial.

* Structura repetitiva cu numar cunoscut de operatii: "pentru <variabila> <- <valoare | variabila>, <valoare | variabila>, <valoare | variabila>"
  * Functia process_for_loop proceseaza structurile repetitive cu numar cunoscut de operatii, verificand daca iteratorul exista deja in vectorul cu variabile. Acesta proceseaza diferit iteratorul, limita si incrementul in functie de folosirea variabilelor sau a valorilor literale.

* Atribuirea valorilor variabilelor: "<variabila> <- <valoare> | <operatii>"
  * Functia process_assignment verifica daca variabila este declarata prima oara si o adauga intr-un vector ce tine evidenta tuturor variabilelor. In caz contar va verifica doar erorile de sintaxa.



## Inainte de rezultatul final

* Se verifica daca sunt prezente in program destule cuvinte cheie de inchidere a structurilor repetitive sau a structurilor logice ("stop", respectiv "pana cand/cat timp").
* In cazul in care nu sunt prezente destule (sau daca sunt prea multe) va fi semnalata o eroare si programul se va termina fara a afisa rezultatul.



## Rezultatul final

* Programul va scrie in fisierul ales la inceput (sau in fisierul "main.cpp" in directorul curent in caz contrar) rezultatul compilarii din Pseudo++ in C++.



## Structura programului
* Programul este impartit in 3 fisiere: main.py, processor.py, preprocessor.py si helpers.py pentru structurarea mai eficienta si logica a codului.
* Acestea comunica transmit informatii de stare intre ele prin intermediul parametrului Counter, definit in helpers.py, care contine starea curenta programului.

* main.py
  * Consta in afisarea interfetei catre utilizator si in invocarea anumitor functii din celelalte fisiere, cat si afisarea rezultatului final.

* preprocessor.py
  * Contine toate functiile de preprocesare ale programului folosite in prima etapa a acestuia.

* processor.py
  * Contine toate functiile de procesare a linilor, inclusiv verificarea majoritatii sintaxei si tinerea evidentei variabilelor (numite in cod "identificatori")

* helpers.py
  * Contine definitia multor clase si functii adjuvante folosite in celelalte fisiere, cum ar fi toate clasele de erori, Counter, Identifier si lista de cuvinte cheie


