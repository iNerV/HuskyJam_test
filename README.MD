#### Note:
Please use `python-3.5+`

## Installation

#### 1.
You should already know what is [virtualenv](http://www.virtualenv.org/). So, simply create it for your own enviroment.
````bash
$ mkdir ~/.virtualenvs
$ python3 -m venv ~/.virtualenvs/HuskyJamTest
$ source ~/.virtualenvs/HuskyJamTest/bin/activate
````
#### 2.
To install  *requirements.txt*, simply type:

`$ pip install -r requirements.txt`

#### 3.

`$ python manage.py runserver` для запуска дев. сервера

`$ python manage.py test` для запуска тестов

`/` стартовая страница с которой можно перейти в к выобру отделения, либо напрямую к выбору доктора к которому необходимо записаться

`/departments` - страница со всеми больничными отделениями, можно перейти в нужное отделение и выбрать доктора для записи к нему, только из списка докторов этого отделения

`/departments/{:id}` - страница отделения, со списком всех докторов этого отделения

`/doctors` - страница со списком всех докторов больницы, можно сразу перейти к записи к нужному доктору

`/doctors/{:id}` - страница записи к доктору

`/sucess` - страница на которую редеректит при удачной попытуке записаться к доктору
