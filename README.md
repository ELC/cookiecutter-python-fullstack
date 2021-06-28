# CookieCutter Python FullStack

This project allows you to automatically generate all the boilerplate code and files for a Full Stack, modern Python Web App, with different options to choose for backends, frontends, databases and web servers.

The project follows the [3-tier Architecture](https://en.wikipedia.org/wiki/Multitier_architecture), meaning that each layer is decouple and you can swap front-ends, back-ends and databases seemlessly.

Contributions are wellcome!

## Why should I use it?

- Because connecting Back End and Front End is not trivial sometimes.
- Because Python provides different ways to do things and it is good to try something new.
- To learn how to use different tools to do the same job and evaluate alternatives.
- To learn about the advantages of decouple systems (3-Layered Architecture)
- Because **all possible configurations** were tested using [Pytest](https://docs.pytest.org/en/latest/) in different versions of Python so you can be sure it works out of the box. 
- No Vendor Lock in, once you use the template, you can modify the result in any way you want, this is just a kick off.

## Getting Started

To use this template you need cookiecutter, if you don't know what it is, check the [2 minute introduction by CalmCode](https://calmcode.io/cookiecutter/the-problem.html). Then install it via pip as:

```
pip install cookiecutter
```

Then, to generate your custom project simply run:

```
cookiecutter https://github.com/ELC/cookiecutter-python-fullstack.git
```

## Run Your Project

You can run the project directly on your local PC or in a container using Docker

### Without Docker

You will need [invoke](http://www.pyinvoke.org/) to run the project install it by running

```
pip install invoke
```

Then, simply run the following command inside the project folder

```
invoke buildAndServe
```

### Without Docker

An alternative approach is to use [Docker](https://www.docker.com/), you will need the Docker engine running. Go with the terminal to the project folder and run:

```
docker build --tag <your_tag> .
```

## Know the possibilities

This project offers different alternatives for each of the layers. **All possible combinations have been tested**

### Front-End

The front-end is taken from the 2021 edition of the Front-End Crash Course by Traversy Media

- **[Vue 3](https://v3.vuejs.org/)**: Vue.js is an open-source model–view–viewmodel front end JavaScript framework for building user interfaces and single-page applications. It was created by Evan You, and is maintained by him and the rest of the active core team members - [Full Tutorial on Youtube](https://www.youtube.com/watch?v=qZXt1Aom3Cs)
- **[React](https://reactjs.org/) (with WebHooks)**: React (also known as React.js or ReactJS) is a free and open-source front-end JavaScript library for building user interfaces or UI components. It is maintained by Facebook and a community of individual developers and companies - [Full Tutorial on Youtube](https://www.youtube.com/watch?v=w7ejDZ8SWv8&t=2483s)
- **[Angular 11](https://angular.io/)**: Angular is a TypeScript-based free and open-source web application framework led by the Angular Team at Google and by a community of individuals and corporations - [Full Tutorial on Youtube](https://www.youtube.com/watch?v=3dHNOWTI7H8)

### Back-End
* [Flask](http://flask.pocoo.org/) on [Python 3](https://python.org) as the web backend

More comming soon...

### Databases

To avoid extra complexity and setup, all the databases included are embedded, meaning, no server-client is needed. Everything happens inside Python.

- **SQL by [SQLite](https://www.sqlite.org/)**: SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. SQLite is the most used database engine in the world
- **NoSQL (Document) by [TinyDB](https://tinydb.readthedocs.io/en/latest/)**: TinyDB is a lightweight document oriented database optimized for your happiness. It's written in pure Python and has no external dependencies.
- **NoSQL (Key-Value/Cache) by [DiskCache](http://www.grantjenks.com/docs/diskcache/)**: DiskCache is an Apache2 licensed disk and file backed cache library, written in pure-Python, and compatible with Django. There’s no need for a C compiler or running another process.
- **Object-Based by [ZODB](https://zodb.org/en/latest/)**: The Zope Object Database (ZODB) is an object-oriented database for transparently and persistently storing Python objects. Features include transactions, history/undo, built-in caching, and more.

### WebServers

* [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/PythonModule.html): The uWSGI project aims at developing a full stack for building hosting services.
* [Waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/): Waitress is meant to be a production-quality pure-Python WSGI server with very acceptable performance. It has no dependencies except ones which live in the Python standard library.
