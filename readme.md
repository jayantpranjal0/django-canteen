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




<!-- Next Change:

3. Add Functionality to order (add to cart and fast checkout)
4. Add functionlity for canteenwala to have an UI for order
5. Add functionality for user to get random 4 digit number for order collection
6. Add functionality for partial order collection




 -->