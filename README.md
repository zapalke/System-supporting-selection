# EN - Decision support system for choosing a study field
## Overview
This repository contains an application created as an engineering thesis called "Decision support system for choosing a field of study" in the field of Systems Engineering at the Wrocław University of Science and Technology. It uses the Django web framework along with data collected from 9 Polish universities to create a DSS that helps the user choose a field of study (first and second cycle). Two systems have been implemented in the application, the first is a list view of all those fields available in the database, the second uses a dedicated algorithm that selects the field of study based on the user's preferences.

## Installation 
To install launch the app do the following:
1. Clone the repository.
2. Create a virtual enviroment for Python 3.10 (it might work with different version) with **python -m venv path/to/new/venv**
3. Install all required packages from **requirements.txt**
4. Go to **/System-supporting-selection/field_of_studies**
5. Launch app with **python manage.py runserver**
6. App will be avielable at **localhost:8000**

## System implemented into the app
### List view with filters
By using navbar or directly from the main page you can access a list which contains all study fields in database (currently there are about 67 fields from 9 universities). The view is paginated by 15 elements and allows user to use filters in order to look for the fields that are best suted for them. Each study field contains following informations:
- Name of study field
- Exam subjects required to be recruited for a given field of study (also containing alternative subjects. For example field X requires Polish AND mathematics OR informatics)
- Which degree you can get (engineering degree, bachelor's degree, long-cycle master's degree, master's degree)
- Univeristy
- Where the univeristy is located
- What rank is the university in Perspektywy ranking (https://2023.ranking.perspektywy.pl/ranking/ranking-uczelni-akademickich)
- Description
- Link to the official site of the study field

### Decision support system with rank method
DSS for this app is based on characteristics of study fields. Each field contains few attributes that describe some of its characteristics, from 0 (characteristic does not belong to field, therefore is not added), to 1 (characteristic strongly belongs to given field). The algorythm in its simplified version works like this:
1. Ask user about what degree is  he looking for (I or II)
2. Ask user which subjects he took at high school leaving exam (user can skip that part)
3. Display 10 attributes for user to choose from.
4. Attributes are divided into two lists, first one containg attributes that user choose, and second one containg the ones that were not choosen.
5. New attributes to display will be semi-random. Most of them will come from similar attributes (based on which were connected to other field)
6. Repeat points 3-5 few times
7. Finally, the matching index is calculated for each item, which is the percentage of the feature values selected from all features that were displayed

# PL - System wspomagania decyzji przy wyborze kierunku studiów
## Przegląd
W repozytorium znajduje się aplikacja stworzona w ramach pracy inżynierskiej o nazwie „System wspomagania decyzji przy wyborze kierunku studiów” na kierunku Inżynieria Systemów na Politechnice Wrocławskiej. Wykorzystuje framework sieciowy Django wraz z danymi zebranymi z 9 polskich uczelni, aby stworzyć DSS, który pomaga użytkownikowi w wyborze kierunku studiów (pierwszego i drugiego stopnia). W aplikacji zaimplementowano dwa systemy, pierwszy to widok listy wszystkich kierunków dostępnych w bazie, drugi wykorzystuje dedykowany algorytm, który dobiera kierunek studiów na podstawie preferencji użytkownika.

## Instalacja
Aby zainstalować, uruchom aplikację, wykonaj następujące czynności:
1. Sklonuj repozytorium.
2. Utwórz wirtualne środowisko dla Pythona 3.10 (może działać z inną wersją) za pomocą **python -m venv path/to/new/venv**
3. Zainstaluj wszystkie wymagane pakiety z **requirements.txt**
4. Przejdź do **/System-supporting-selection/field_of_studies**
5. Uruchom aplikację za pomocą **python zarządzaj.py runserver**
6. Aplikacja będzie dostępna pod adresem **localhost:8000**

## System zaimplementowany w aplikacji
### Widok listy z filtrami
Za pomocą belki nawigacyjnej lub prosto ze strony głównej możesz uzyskać dostęp do listy zawierającej wszystkie kierunki studiów w bazie danych (obecnie jest około 67 kierunków z 9 uniwersytetów). Widok jest podzielony na strony po 15 elementów każda i pozwala na użycie filtrów w celu wyszukania najbardziej odpowiednich dla siebie pól. Każde pole badania zawiera następujące informacje:
- Nazwa kierunku studiów
- Przedmioty egzaminacyjne wymagane do rekrutacji na dany kierunek studiów (zawierające także przedmioty alternatywne. Np. kierunek X wymaga języka polskiego ORAZ matematyki LUB informatyki)
- Jaki stopień możesz uzyskać (inżynier, licencjat, jednolite magisterskie, magisterskie)
- Uniwersytet
- Gdzie znajduje się uniwersytet
- Jaką pozycję zajmuje uczelnia w rankingu Perspektywy (https://2023.ranking.perspektywy.pl/ranking/ranking-uczelni-akademickich)
- Opis
- Link do oficjalnej strony kierunku studiów

### System wspomagania decyzji metodą rankingową
DSS dla tej aplikacji opiera się na charakterystykach kierunków studiów. Każdy kierunek zawiera kilka atrybutów opisujących niektóre jego cechy, od 0 (cecha nie należy do kierunku, dlatego nie jest dodawana), do 1 (cecha silnie należy do danego kierunku). Algorytm w wersji uproszczonej działa następująco:
1. Zapytaj użytkownika o to, jakiego stopnia studiów szuka (I lub II)
2. Zapytaj użytkownika, jakie przedmioty zdawał na maturze (użytkownik może pominąć tę część)
3. Wyświetl 10 atrybutów do wyboru przez użytkownika.
4. Atrybuty podzielone są na dwie listy, pierwsza zawiera atrybuty wybrane przez użytkownika, druga zaś te, które nie zostały wybrane.
5. Nowe atrybuty do wyświetlenia będą półlosowe. Większość z nich będzie pochodzić z podobnych atrybutów (na podstawie których zostały połączone z innymi kierunkami studiów)
6. Powtórz punkty 3-5 kilka razy
7. Na koniec dla każdej pozycji obliczany jest wskaźnik dopasowania, który stanowi procent wartości cech wybranych spośród wszystkich wyświetlonych cech

