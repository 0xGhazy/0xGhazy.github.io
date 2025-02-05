---
created: 2022-10-10
title: "Singleton Design Pattern"
description: "Singleton Design Pattern in a nutshell...."
layout: post
tags: [singleton]
category: [Design Patterns]
image:
  path: /assets/img/blogs/singleton-design-pattern.png
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

Hello world, Hossam is here, welcome to my first blog in the Graduation Project Diary series, in this blog I try to explain and discuss new things that I have learned during the final year @ BFCAI ❤️.

I write this post on 10/10/2022 at 12:40 AM, in this post I’ll talk about one problem that I face during writing some code in the project, The problem is that I was working on a Database API which is a python module that connect to the database and provide me with a formal interface to interact with the project database, it’s an approach that I’m using for a while, Example of this API you can see [0xGhazy/PyPass.](https://github.com/0xGhazy/PyPass)

This API will create a new instance every time it’s invoked, which is not a good practice, in this approach we consume a shared resource such as a database, file, and any similar idea. How can I deal with this kind of problem?

here we can use one of the creational design patterns called Singleton design pattern, Let’s talk about it 😃.

### What is the design patterns?

**Design patterns** are typical solutions to commonly occurring problems in software design. They are like pre-made blueprints that you can customize to solve a recurring design problem in your code.

Our learning and use of design patterns, improve our view of problems and strengthens our skill in solving design-related software problems.

**Singleton** is a creational design pattern that lets you ensure that a class has only one instance, while providing a global access point to this instance.

### Singleton Pros

Singleton design pattern solve two kind of problems:
1- **Ensure that a class has just a single instance**. (we will see this in the Demo)
2- **Provide a global access point to that instance**.

### Singleton Cons

As always, nothing is perfect, Singleton has a problem with violating the principle of Single Responsibility, Because the class has two distinct responsibilities:

- Making sure that only one instance can be created.
- The core functionality of the class - accessing database for an example.

### Python Demo

```python
class MainClass:

    def __init__(self):
        print("Create New Instance of MainClass")

object2 = MainClass()
object1 = MainClass()
object3 = MainClass()
```

The previous code i have a simple class called `MainClass` which have the `__init__()` method only for the explaining purposes. By running this code we get the following output.

![1](https://user-images.githubusercontent.com/60070427/195465122-61ad47e2-757b-4011-b1c6-66a6c1a7a82b.png)

I think you guessed the output 99% true, we have a new instance every time we create a `MainClass` object.

### Solution

Lets see who to overcome this problem with the Singleton implementation. First, how does Singleton work and be implemented?

First we have the following steps to implement the Singleton:
1- Private static variable that holds the Singleton instance.
2- Creating a public method that allow creating a Singleton instance. (This Method can't create new object if the private variable that we mentioned earlier is not equal None/null or whatever the value we init it with.)
3- Returning the new created instance.

**Python Code:**

```python
class Singleton(object):
	# Flag variable to check if instance is created or not
    _instance = None

    def __new__(cls):
	    # Check if we have any Singleton instance in memory
        if cls._instance is None:
            print('Creating the Singleton object')
			# Creating an instance of the Singleton class
            cls._instance = super(Singleton, cls).__new__(cls)
            # Put any initialization here.
            # Here we Overwrite the __init__ method
        # Return the new instance
        return cls._instance

o1 = Singleton()
o2 = Singleton()
o3 = Singleton()
```

![2](https://user-images.githubusercontent.com/60070427/195465119-27b95bea-4d3a-4c3d-b301-5a32bbf7c3f3.png)

As you can see in the previous output image, we have only one instance created even though we are calling the constrictor 3 times. and this is what I looking for in my case 😃.

I hope you have benefited from this simple article, if you find this content useful, share it with your friends to spread the benefit among them. You For reading 💙.

## References

- [Singleton - refactoring.guru](https://refactoring.guru/design-patterns/singleton)
- [The Singleton Pattern](https://python-patterns.guide/gang-of-four/singleton/)
- [Singleton Pattern Pitfalls - Vojtech Ruzicka's Programming Blog](https://www.vojtechruzicka.com/singleton-pattern-pitfalls/)
