# Setup

The first thing to do is to clone the repository:

```sh
$ https://github.com/jayantpranjal0/Canteen-App.git
$ cd django-canteen
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd django-canteen
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.



<!-- 

Things left to complete basic:
1. OTP based orders verifications
2. Update on every item prepraration and order and delivery


Migrate the model to just keep count of meals with the user
This is a different kind of project
 -->


 <!-- 
 Further tasks:
 Optimizations
  -->