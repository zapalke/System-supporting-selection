# EN - Decision support system for choosing a study field

This is a web application that helps students choose their field of study based on their preferences, skills, and interests. The application uses a Django framework and a SQLite3 database to provide a user-friendly interface and a reliable backend. The application allows users to fill in a questionnaire, view the results of the analysis, and browse the available fields of study. Keep in mind that app was creaded in polish.

## Installation and data loading

To install and run the application, you need to have Python 3.11 or higher and pip installed on your system.  Then, follow these steps:

1. Clone the repository from GitHub: `git clone https://github.com/zapalke/System-supporting-selection.git`
2. Navigate to the project directory: `cd System-supporting-selection`
3. Create and activate a virtual environment: `python -m venv venv` and `source venv/bin/activate` / `venv/Scripts/activate` (Windows)
4. Install the required packages: `pip install -r requirements.txt`
5. Run the server: `python manage.py runserver`
6. Open the application in your browser: `http://127.0.0.1:8000/`

## Usage and features

To use the application, you do not need to register an account. It consists two supporitng system for choosing field of study. The first one is a comprehensive browser of fields. The second one is a DSS that uses data provided by the user to make a candidate profile and then weighted sum model and TOPSIS method to calculate best fitted study fields. To use the system you should:
- Grade the importance of 5 criterums.
- Fill in a questionnaire that asks you about your preferences, skills, and interests. The questionnaire consists of multiple-choice questions and takes about 10 minutes to complete.
- View the results of the analysis that shows you the best matching fields of study for you.  You can see the score and the description of each field of study, as well as the link to the official website of the university that offers it.

## License and authors

This project is licensed under the MIT License. Please refer to the [LICENSE] file for more information. This project was created by [zapalke], a student of the Wrocław University of Science and Technology, for the needs of an engineering project titled "Decision support system for choosing a field of study."

# PL - System wspomagania decyzji przy wyborze kierunku studiów

Jest to aplikacja webowa, która pomaga studentom wybrać kierunek studiów na podstawie ich preferencji, umiejętności i zainteresowań. Aplikacja wykorzystuje framework Django i bazę danych SQLite3, aby zapewnić przyjazny dla użytkownika interfejs i niezawodne zaplecze. Aplikacja pozwala użytkownikom wypełnić kwestionariusz, zobaczyć wyniki analizy i przeglądać dostępne kierunki studiów.

## Instalacja i ładowanie danych

Aby zainstalować i uruchomić aplikację, musisz mieć zainstalowane Python 3.11 lub wyższy i pip na swoim systemie. Następnie wykonaj następujące kroki:

1. Sklonuj repozytorium z GitHuba: `git clone https://github.com/zapalke/System-supporting-selection.git`
2. Przejdź do katalogu projektu: `cd System-supporting-selection`
3. Utwórz i aktywuj wirtualne środowisko: `python -m venv venv` i `source venv/bin/activate` (Linux) / `venv/Scripts/activate` (Windows)
4. Zainstaluj wymagane pakiety: `pip install -r requirements.txt`
5. Uruchom serwer: `python manage.py runserver`
6. Otwórz aplikację w przeglądarce: `http://127.0.0.1:8000/`

## Użytkowanie i funkcje

Aby korzystać z aplikacji, nie musisz rejestrować konta. Składa się ona z dwóch systemów wspomagających wybór kierunku studiów. Pierwszy to kompleksowa przeglądarka kierunków. Drugi to system wspomagania decyzji, który wykorzystuje dane podane przez użytkownika, aby stworzyć profil kandydata, a następnie model sumy ważonej i metodę TOPSIS, aby obliczyć najlepiej dopasowane kierunki studiów. Aby skorzystać z systemu, powinieneś:

- Oceniać wagę 5 kryteriów.
- Wypełnić kwestionariusz, który pyta cię o twoje preferencje, umiejętności i zainteresowania. Kwestionariusz składa się z pytań wielokrotnego wyboru i zajmuje około 10 minut.
- Zobaczyć wyniki analizy, która pokazuje ci najlepiej pasujące do ciebie kierunki studiów. Możesz zobaczyć wynik i opis każdego kierunku studiów, a także link do oficjalnej strony internetowej uczelni, która go oferuje.

## Licencja i autorzy

Ten projekt jest licencjonowany na licencji MIT. Więcej informacji znajdziesz w pliku [LICENSE]. Ten projekt został stworzony przez [zapalke], studenta Politechniki Wrocławskiej, na potrzeby pracy inżynierskiej zatytuowanej "System wspomagający wybór kierunków studiów".

