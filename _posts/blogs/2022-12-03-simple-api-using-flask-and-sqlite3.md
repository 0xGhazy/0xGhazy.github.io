---
created: 2022-12-03
title: "Creating Simple REST API Using Python Flask, SQLite3, and Postman"
description: "Implementing CRUD API using python flask and SQLite3."
layout: post
tags: [backend, python, rest]
category: [Backend]
image:
  path: /assets/img/blogs/grad3-thumbnail.png
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

Hello world, Hossam is here, welcome to my 3rd blog in the Graduation Project Diary series, in this blog I try to explain and discuss new things that I have learned during the final year @ BFCAI ❤️. In this post I'll try to explain how to implement Python Flask API for my project teammates to be aware of this topic and do their tasks 😃

# Introduction

Lets start with building Simple CRUD API using Flask and SQLite3, our example project we will create a `Books` table that we can Create, Retrieve, Update, Delete (CRUD). i also will mention how to implement database API that provide you with simple way to interact with database in an easy, and readable way. Our project will handle requests coming from the user via HTTP, and then we will apply this to the database.
lets start by creating project directory and Database. I'll use this structure.

```
/API
	/cores
		__inti__.py
		database_api.py
		booksDB.db
	api.py
```

# Building Database API

In this section I'll build python class called `DatabaseAPI` to be my interface and formal way to interact with my SQlite3 database. in this approach our API/application code will be clean and free of SQL syntax because all database syntax and operation will be handled by `DatabaseAPI` which is good for encapsulation and abstraction. lets start with the `__init__(self)` method

### Database Schema

building the Books Table with the following simple code

```sql
CREATE TABLE "Books" (
	"Id"	INTEGER UNIQUE,
	"title"	TEXT NOT NULL,
	"author"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"pages"	INTEGER NOT NULL,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
```

### Init method`

here in the `__init__()` method we can pass the database name to be connected with, in this approach i can connect to multiple database if i have to, then we created a method to connect to the passed database name to be ready to interact with this resource.

```python
import os
import sqlite3
from typing import List

class DatabaseAPI:

    def __init__(self, db_name) -> None:
        os.chdir(os.path.dirname(__file__))
        self._db_name = db_name
        self._connection = self.db_connect()
```

### Database connection handler method

that returns sqlite3 connection if the connection process goes true.

```python
    def db_connect(self) -> sqlite3:
        try:
            return sqlite3.connect(self._db_name)
        except Exception as error:
            raise Exception(f"[-] Error Message:\n{error}\n")
```

### Getting all books

Getting all books from database and `Books` table by using `SELECT *` and return list of results.

```python
    def get_all_books(self) -> List[list]:
        cursor = self._connection.cursor()
        response = cursor.execute(f"SELECT * FROM Books;")
        return list(response)
```

### Getting Book by id

like the previous code sample but with adding the `WHERE` keyword to filter results for the passing book `id`.

```python
    def get_book_by_id(self, id) -> List:
        cursor = self._connection.cursor()
        response = cursor.execute(f"SELECT * FROM Books WHERE Id = {id};")
        return response
```

### Insert and update a Book

i implement 2 methods that takes a book object/dict and passing it to the `INSERT` statement then commit this action to the database, another method do the same but it perform update action using `SET` statement with the book id to update a specific book.

```python
    def insert_book(self, book_data: dict):
        cursor = self._connection.cursor()
        cursor.execute(f"""
        INSERT INTO Books (title, author, description, pages)
	    VALUES ('{book_data['title']}',
			    '{book_data['author']}',
			    '{book_data['description']}',
			    '{book_data['pages']}');""")
        self._connection.commit()

     def update_book(self, id: int, new_data: dict):
        cursor = self._connection.cursor()
        cursor.execute(f"""
        UPDATE Books SET title = '{new_data['title']}',
                         author = '{new_data['author']}',
                         description = '{new_data['description']}',
                         pages = '{new_data['pages']}'
        WHERE Id = {id};""")
        self._connection.commit()
```

### Deleting Book by id

```python
    def delete_book(self, id):
        cursor = self._connection.cursor()
        cursor.execute(f"""DELETE FROM Books WHERE Id = {id};""")
        self._connection.commit()
```

## Put altogether

```python
import os
import sqlite3
from typing import List

class DatabaseAPI:

    def __init__(self, db_name) -> None:
        os.chdir(os.path.dirname(__file__))
        self._db_name = db_name
        self._connection = self.db_connect()

    def db_connect(self) -> sqlite3:
        try:
            return sqlite3.connect(self._db_name)
        except Exception as error:
            raise Exception(f"[-] Error Message:\n{error}\n")

    def get_all_books(self) -> List[list]:
        cursor = self._connection.cursor()
        response = cursor.execute(f"SELECT * FROM Books;")
        return list(response)

    def get_book_by_id(self, id) -> List:
        cursor = self._connection.cursor()
        response = cursor.execute(f"SELECT * FROM Books WHERE Id = {id};")
        return response

    def insert_book(self, book_data: dict):
        cursor = self._connection.cursor()
        cursor.execute(f"""
        INSERT INTO Books (title, author, description, pages)
        VALUES ('{book_data['title']}',
		        '{book_data['author']}',
		        '{book_data['description']}',
		        '{book_data['pages']}');""")
        self._connection.commit()

    def update_book(self, id: int, new_data: dict):
        cursor = self._connection.cursor()
        cursor.execute(f"""
        UPDATE Books SET title = '{new_data['title']}',
                         author = '{new_data['author']}',
                         description = '{new_data['description']}',
                         pages = '{new_data['pages']}'
        WHERE Id = {id};""")
        self._connection.commit()

    def delete_book(self, id):
        cursor = self._connection.cursor()
        cursor.execute(f"""DELETE FROM Books WHERE Id = {id};""")
        self._connection.commit()
       

if __name__ == "__main__":
    databaseObj = DatabaseAPI("booksDB.db")
```

# Building Flask API

## Init the flask Application

```python
# Importing Required classes
from flask import Flask, request

# init Flask application
app = Flask(__name__)

# Simple Endpoint to return Hello world message
@app.route("/hello", methods=["GET"])
def home():
    return "Hello World!"

# Running your application with debugging mode on
app.run(debug=True)
```

using the previous simple lines of code, we have created an endpoint `hello` which handle `GET` request HTTP method and return the `Hello World` message, lets test this API by running our application and test the endpoint using `Postman`.

![Pasted image 20221203145707](https://user-images.githubusercontent.com/60070427/205449640-491f79cb-063c-437a-87d2-1f48c28937cb.png)

Our application is running on Port `5000` in the following URL `http://127.0.0.1:5000` lets send Get Request to our application at the following `http://127.0.0.1:5000/hello` endpoint.

![Pasted image 20221203145945](https://user-images.githubusercontent.com/60070427/205449654-87ea1b88-3280-4b4b-a147-e1cbfa7ba73e.png)

## Handling GET requests

Lets create 2 endpoints to handle the two type of GET requests, our user may wanna list all books or get one book by it's id so ew need to implement this two situations separately.

### Get Book by id

getting book from the Books table by it's passed id parameter after `books/` in url

```python
@app.route("/books/<id>", methods=["GET"])
def get_book_by_id(id: int) -> str:
    database_api = DatabaseAPI("booksDB.db")
    result = list(database_api.get_book_by_id(id))
    response = {
        "data":{
            "result": result[0]
        }
    }
    return response
```

### Get all Books

the following code will handle all `GET` requests for `/books` end point and return all books that exist in Books table.

```python
@app.route("/books", methods=["GET"])
def get_all_books() -> list:
    database_api = DatabaseAPI("booksDB.db")
    response = {
        "data":{
            "result": database_api.get_all_books()
        }
    }
    return response
```

## Handling POST requests

post requests for adding new book to our database, in this section for `POST` and `PUT` methods we need to read the passed data in the request body, we can do that by using `request` from flask class then access the `data` key like the following line

```python
request_body = json.loads(request.data.decode())
```

we load the data in JSON format to be accessible for us as a dict type. after getting needed body parameters we can add new book to the database like the following.

```python
@app.route("/books", methods=["POST"])
def add_new_book() -> str:
    database_api = DatabaseAPI("booksDB.db")
    # Reading request body data in json format
    request_body = json.loads(request.data.decode())
    new_book = {
        "title": request_body["title"],
        "author": request_body["author"],
        "description": request_body["description"],
        "pages": request_body["pages"],
    }
    # Add book to database
    database_api.insert_book(new_book)
    return jsonify(new_book)
```

## Handling PUT requests

Returning the updated record after operation done successfully. Note that we pass `id` after `/books/` to apply the update operation to that specific book.

```python
@app.route("/books/<id>", methods=["PUT"])
def update_book(id: int) -> str:
    database_api = DatabaseAPI("booksDB.db")
    # Reading request body data in json format
    request_body = json.loads(request.data.decode())
    new_book = {
        "title": request_body["title"],
        "author": request_body["author"],
        "description": request_body["description"],
        "pages": request_body["pages"],
    }
    # Add book to database
    database_api.update_book(id, new_book)
    return jsonify(new_book)
```

## Handling DELETE requests

Deleting book by it's id then returning the deleted book record.

```python
@app.route("/books/<id>", methods=["DELETE"])
def delete_book(id: int) -> str:
    database_api = DatabaseAPI("booksDB.db")
    # Reading request body data in json format
    selected_book = list(database_api.get_book_by_id(id))
    response = {
        "data":{
            "result": selected_book[0]
        }
    }
    database_api.delete_book(id)
    return response
```

## Put altogether

at the end our API looks like the following

```python
from flask import Flask, request, jsonify
import json
from cores.database_api import DatabaseAPI

# init Flask application
app = Flask(__name__)

# Simple Endpoint to return Hello world message
@app.route("/hello", methods=["GET"])
def home():
    return "Hello World!"

@app.route("/books", methods=["GET"])
def get_all_books() -> list:
    database_api = DatabaseAPI("booksDB.db")
    response = {
        "data":{
            "result": database_api.get_all_books()
        }
    }
    return response

@app.route("/books/<id>", methods=["GET"])
def get_book_by_id(id: int) -> str:
    database_api = DatabaseAPI("booksDB.db")
    result = list(database_api.get_book_by_id(id))
    response = {
        "data":{
            "result": result[0]
        }
    }
    return response

@app.route("/books", methods=["POST"])
def add_new_book() -> str:
    database_api = DatabaseAPI("booksDB.db")
    # Reading request body data in json format
    request_body = json.loads(request.data.decode())
    new_book = {
        "title": request_body["title"],
        "author": request_body["author"],
        "description": request_body["description"],
        "pages": request_body["pages"],
    }
    # Add book to database
    database_api.insert_book(new_book)
    return jsonify(new_book)

@app.route("/books/<id>", methods=["PUT"])
def update_book(id: int) -> str:
    database_api = DatabaseAPI("booksDB.db")
    # Reading request body data in json format
    request_body = json.loads(request.data.decode())
    new_book = {
        "title": request_body["title"],
        "author": request_body["author"],
        "description": request_body["description"],
        "pages": request_body["pages"],
    }
    # Add book to database
    database_api.update_book(id, new_book)
    return jsonify(new_book)

@app.route("/books/<id>", methods=["DELETE"])
def delete_book(id: int) -> str:
    database_api = DatabaseAPI("booksDB.db")
    # Reading request body data in json format
    selected_book = list(database_api.get_book_by_id(id))
    response = {
        "data":{
            "result": selected_book[0]

        }
    }
    database_api.delete_book(id)
    return response

# Running your application with debugging mode on
app.run(debug=True)
```

# Try Your new API

Using the Postman application we will try and test our Implementation.

### Test POST Method

- simple test data (`raw json data`)

```json
{
  "title": "Building Powerful API Using Flask",
  "author": "Hossam hamdy",
  "description": "DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION",
  "pages": 100
}
```

- URL: http://127.0.0.1:5000/books
- Result:
  ![Pasted image 20221203165017](https://user-images.githubusercontent.com/60070427/205449668-00eab597-34fa-4336-893a-56ff9cb1a9a2.png)

![Pasted image 20221203165238](https://user-images.githubusercontent.com/60070427/205449686-1e192496-26d3-494a-8af3-03593209b794.png)

### Test GET Method

As we see in the previous test our book is added successfully, now lets try to get this book by id `4`

- URL: http://127.0.0.1:5000/books/4
- Result:
  ![Pasted image 20221203165445](https://user-images.githubusercontent.com/60070427/205449703-09f9e37e-6df7-447d-9123-8f3c11d311e8.png)

### Testing PUT Method

Lets update the inserted book to be using `NodeJS` instead of python.

- simple test data (`raw json data`)

```json
{
  "title": "Building Powerful API Using NodeJS",
  "author": "hossam hamdy",
  "description": "DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION",
  "pages": 100
}
```

- URL: http://127.0.0.1:5000/books/4
- Result:

![Pasted image 20221203172407](https://user-images.githubusercontent.com/60070427/205449729-1f4e0630-2366-4101-ae4d-a2a37762e984.png)

![Pasted image 20221203172424](https://user-images.githubusercontent.com/60070427/205449756-717e9c29-5322-4f89-9442-4cf21e24d4a9.png)

### Testing DELETE Method

![Pasted image 20221203172719](https://user-images.githubusercontent.com/60070427/205449771-53944eeb-ea85-4a4e-a445-cfa745000027.png)

congrats our API is ready and built successfully 😃.

# Appendix

Most modern web applications expose APIs that clients can use to interact with the application. A well-designed web API should aim to support:

- **Platform independence**. Any client should be able to call the API, regardless of how the API is implemented internally. This requires using standard protocols, and having a mechanism whereby the client and the web service can agree on the format of the data to exchange.
- **Service evolution**. The web API should be able to evolve and add functionality independently from client applications. As the API evolves, existing client applications should continue to function without modification. All functionality should be discoverable so that client applications can fully use it.

You can use this resource for building robust, well-designed APIs [Link](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)

Thank You for reading 😃.
