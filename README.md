# Decision support system for choosing a study field
## Overview
In this repository there is an application created as an engineering work called "Decision support system for choosing a study field" on Systems Engineering at Wroclaw University of Science and Technology. It uses a Django web framework along with data gathered from 9 polish universities to create a DSS which helps user with choosing a study field (I & II degree). There are 2 system implemented into the app, first one is a list view of all avielable in database and second one uses a dedicated algorythm which chooses a study field based on user's preferences.

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
At **localhost:8000/FieldListView** (or using navbar) you can access a list which contains all study fields in database (currently there are about 67 fields from 9 universities). Each study field contains following informations:
- Name of study field
- Exam subjects required to be recruited for a given field of study (also containing alternative subjects. For example field X requires Polish AND mathematics OR informatics)
- Which degree you can get (engineering degree, bachelor's degree, long-cycle master's degree, master's degree)
- Univeristy
- Where the univeristy is located
- What rank is the university in Perspektywy ranking (https://2023.ranking.perspektywy.pl/ranking/ranking-uczelni-akademickich)
- Description
- Link to the official site of the study field
The view is paginated by 15 elements and allows user to use filters in order to look for the fields that are best suted for them.
### Decision support system with rank method
DSS for this app is based on characteristics of study fields. Each field contains few attributes that describe some of its characteristics, from 0 (characteristic does not belong to field, therefore is not added), to 1 (characteristic strongly belongs to given field). The algorythm in its simplified version works like this:
1. Ask user about what degree is  he looking for (I or II)
2. Ask user which subjects he took at high school leaving exam (user can skip that part)
3. Display 10 attributes for user to choose from.
4. Attributes are divided into two lists, first one containg attributes that user choose, and second one containg the ones that were not choosen.
5. New attributes to display will be semi-random. Most of them will come from similar attributes (based on which were connected to other field)
6. Repeat points 3-5 few times
7. Finally, the matching index is calculated for each item, which is the percentage of the feature values selected from all features that were displayed

