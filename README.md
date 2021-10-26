# Teacher Directory app
This is a lightweight teacher directory app that contains data about teachers.



## Getting Started

	git clone https://github.com/lotfibk97/teachers_directoryapp
  
  Go to directoryapp:
  
  ```cd directoryapp```
  
  Install the necessary packages:
  
  ```pip install -r requirements.txt``` (or ```python -m pip install -r requirements.txt```)
  
  Create the migrations:
  
  ```python manage.py makemigrations``` ```python manage.py makemigrations directory``` (if the first one doesn't work)
  
  Apply them:
  
  ```python manage.py migrate```
  
  If you want to log in
  
  (optional) ```python manage.py createsuperuser```
  
## Usage

Then run the following command:

```python manage.py runserver ```
    
and finally go to your browser and enter the url: 127.0.0.1:8000.    
