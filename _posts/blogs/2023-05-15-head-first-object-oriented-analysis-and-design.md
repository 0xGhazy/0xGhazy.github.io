---
created: 2022-12-03
title: "Head First Object-Oriented Analysis & Design Summary"
description: "Head First Object-Oriented Analysis & Design book summary"
layout: post
tags: [OOA&D, OOP]
category: [Object-Oriented]
image:
    path: /assets/img/blogs/head_first_object_oriented_analysis_and_design.jpg
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

# Chapter 1: Great Software Begins Here

## What is great software from different points of view?

-   The _**customer friend**_ sees that the great software does what the customer wants it to do and doesn't give un expected result when we use it in a new way.
-   The _**Object-Oriented Programming**_ guy sees that the great software has no code duplication, each object controls its own behavior, and finally easy to be extended.
-   The _**Design Pattern**_ guy sees that the great software is what used a tried-and-true design patterns and principles. Objects are loosely coupled, Open for extension but closed for modifications. finally the code in the software must be reusable.
-   A _**Computer science student in BFCAI**_ called Hossam Hamdy -Yes it's me 😀- sees that, great software follows the best design practices and design patterns to not re-invent the wheel again, that software that respects customer requirements but at the same time doesn't ignore the engineering side.

From all of this points mentioned above, The authors provide us a simple approach for writing great software by applying the following 3 steps:

1. **Make sure your software does what the customer wants it to do**
   So here we must make sure that our software is compatible with our customer's requirements/functionalities. No matter how well-designed your application is, If your software functionality does not meet the requirements.
2. **Apply basic OO principles to add flexibility**
   Applying some basic OO principles keeps your application flexible and easy to change without worrying about changes and maintenance.
3. **Strive for a maintainable reusable design**
   Here we can use Design Patterns It's all about reusing and making sure you’re not trying to solve a problem that someone else has already figured out.

## Encapsulation is not only for data hiding

Here I learned a new concept and use of Encapsulation, It's not about bundling data and methods that work on that data within one unit. we can use it to remove duplicated codes too.

Here I'll use the example mentioned in the book in this chapter, our customer wanna create a new application to manage the inventory of his instrument store.

![image](https://github.com/user-attachments/assets/2b208906-b913-4295-b37e-990672b2af99)

Suppose we have this code snippet for a `Guitar` class that represents a real guitar for an instrument store -I'm using `@Data` from lombok to make Guitar class shorter, by adding `@Data` it will implement all getters and setters for the class attributes `@AllArgsConstructor` to generate all attributes constructor-:

```java
@Data
@AllArgsConstructor
public class Guitar {  
    private String serialNumber;
    private double price;
    private Builder builder;
    private String model;
    private Type type;
    private Wood backWood;
    private Wood topWood;
 }
```

Our client needs to be able to search for a guitar that meet the store client specification, Lets implement method that does our client search operation and suppose its `Guitar search(Guitar guitar)`

```java
public class Inventory {
    private List guitars;

	public Inventory() { guitars = new LinkedList(); }

	public void addGuitar(String serialNumber, double price, String builder, String model,
						  String type, String backWood, String topWood) {
		Guitar guitar = new Guitar(serialNumber, price, builder, model, type, backWood, topWood);
		guitars.add(guitar);
	}

	public Guitar getGuitar(String serialNumber) {
		for (Iterator i = guitars.iterator(); i.hasNext(); ) {
			Guitar guitar = (Guitar)i.next();
			if (guitar.getSerialNumber().equals(serialNumber)) {
				return guitar;
			}
		}
		return null;
	}

	public Guitar search(Guitar searchGuitar) {
		for (Iterator i = guitars.iterator(); i.hasNext(); ) {
			Guitar guitar = (Guitar)i.next();

			// Ignore serial number since that’s unique
			// Ignore price since that’s unique

			String builder = searchGuitar.getBuilder();
			if ((builder != null) && (!builder.equals("")) &&
				(!builder.equals(guitar.getBuilder())))
				continue;

			String model = searchGuitar.getModel();
			if ((model != null) && (!model.equals("")) &&
				(!model.equals(guitar.getModel())))
				continue;

			String type = searchGuitar.getType();
			if ((type != null) && (!searchGuitar.equals("")) &&
				(!type.equals(guitar.getType())))
			continue;

			String backWood = searchGuitar.getBackWood();
			if ((backWood != null) && (!backWood.equals("")) &&
				(!backWood.equals(guitar.getBackWood())))
				continue;

			String topWood = searchGuitar.getTopWood();
			if ((topWood != null) && (!topWood.equals("")) &&
				(!topWood.equals(guitar.getTopWood())))
				continue;

			return guitar;
		}
		return null;
	}
}
```

Here is our implementation for `FindGuitarTester` class to test our implementation:

```java
public class FindGuitarTester {

	public static void main(String[] args) {
		// Set up Rick’s guitar inventory
		Inventory inventory = new Inventory();

		initializeInventory(inventory);

		Guitar whatErinLikes = new Guitar("", 0, "fender", "Stratocastor",
		"electric", "Alder", "Alder");

		Guitar guitar = inventory.search(whatErinLikes);
		if (Guitar == null) {
			// print error, can't find anything that match the search criteria
		} else {
			// print we get the guitar you wanna
		}
	}

}
```

Here is the customer `Rick` -owner of the application- start using the application but no result found even if the inventory has the specified guitar with `builder:"Fender"` that meet the customer requirements.

This implementation has some issues:

1. **A lot of string literal comparison**
   Our customer can set the builder to "`fender`", "`Fender`", and "`FeNdEr`" which are all not equal to each other. Yes we can do _toLowerCase()_ or _toUpperCase()_ but this is not the proper solution for all cases.

2. **Client doesn't care about the guitar `serial number` or `price`**
   The store client doesn't care about the serial number or price so he didn't provide it in the search method.

**For ths issue `#1`**:
We can solve it by using `enum` type to define our attribute types, This will prevent miss spilling, letters case, and unexpected values from the store client.

For in the case of `model` we can't use Enums because models vary very much. So here we will use `toLowerCase() / toUpperCase()` instead.

Example of `Wood` enum:

```java
public enum Wood {
    INDIAN_ROSEWOOD,
    BRAZILIAN_ROSEWOOD,
    MAHOGANY,
    MAPLE,
    COCOBOLO,
    CEDAR,
    ADIRONDACK,
    ALDER,
    SITKA;

    public String toString() {
        switch (this) {
            case INDIAN_ROSEWOOD:
                return "Indian Rosewood";
            case BRAZILIAN_ROSEWOOD:
                return "Brazilian Rosewood";
            case MAHOGANY:
                return "Mahogany";
            case MAPLE:
                return "Maple";
            case COCOBOLO:
                return "Cocobolo";
            case CEDAR:
                return "Cedar";
            case ADIRONDACK:
                return "Adirondack";
            case ALDER:
                return "Alder";
            case SITKA:
                return "Sitka";
            default:
                throw new IllegalArgumentException();
        }
    }
}
```

**For ths issue `#2`**:

Her we can separate the guitar main attributes such as [`price`, `serial`] and guitar specifications attributes such as [`builder`, `model`, `type`, `backWood`, `topWood`].

The new Guitar Class code:

```java
@Data
@AllArgsConstructor
public class Guitar {
    private String serialNumber;
    private double price;
    // each guitar object must have a GuitarSpec object to describe it.
    private GuitarSpec guitarSpec;
}
```

The GuitarSpec Class code

```java
public class GuitarSpec {  
    private Builder builder;  
    private String model;  
    private Type type;  
    private Wood backWood;  
    private Wood topWood;  
    public Builder getBuilder() {return builder;}  
    public void setBuilder(Builder builder) {this.builder = builder;}  
    public String getModel() {return model;}  
    public void setModel(String model) {this.model = model;}  
    public Type getType() {return type;}  
    public void setType(Type type) {this.type = type;}  
    public Wood getBackWood() {return backWood;}  
    public void setBackWood(Wood backWood) {this.backWood = backWood;}  
    public Wood getTopWood() {return topWood;}  
    public void setTopWood(Wood topWood) {this.topWood = topWood;}  
 }
```

The new search method code:

```java
public Guitar search(Guitar searchGuitar) {
	for (Iterator i = guitars.iterator(); i.hasNext(); ) {
		Guitar guitar = (Guitar)i.next();
		// Ignore serial number since that’s unique
		// Ignore price since that’s unique
        if (searchGuitar.getBuilder() != guitar.getBuilder())
            continue;

		String model = searchGuitar.getModel().toLowerCase();
		if ((model != null) && (!model.equals("")) && (!model.equals(guitar.getModel().toLowerCase())))
			continue;

		if (searchGuitar.getType() != guitar.getType())
			continue;

		if (searchGuitar.getBackWood() != guitar.getBackWood())
			continue;

		if (searchGuitar.getTopWood() != guitar.getTopWood())
			continue;
	return guitar;
	}

	return null;
}
```

With this approach we have a good design because in the future if we wanna add a new property to the Guitar we don't need to change the guitar class each time, we just need to add it into the `GuitarSpec` and the _search()_ method will do it's job. we separate the application's parts and encapsulate the parts that might `vary/change` away from the parts that will stay the same.

**`Anytime you see duplicate code, look for a place to encapsulate`**.

**Delegation** The act of one object forwarding an operation to another object, to be performed on behalf of the first object. such as _.equals()_ method in java. delegation enables the code reusability and makes it **loosely coupled** (the object has a specific job to do and they do only that job).

---

# Chapter 02: Gathering Requirements

_Requirement_ is a specific thing your system has to do to work correctly. It's about what a particular service should do.

## Listen to the customer

To gather requirements, we need to listen to the customer carefully and pay attention to everything he says about the system wanna have or feature wanna add. In listening phase, we care about **what system has to do?** not **How we'll implement this?**

Focusing on implementation details in this phase is a big mistake that I unfortunately do in meetings. This makes me drop some necessary details in requirements and start thinking about the limitations of used technologies or on the other side start saying "yes it's easy I can implement it and deliver this `feature` in 3 hours" but it's not true at all 😩.

## Create Requirements List

After we listen to the customer requirements, we need to create a list of them as the following.

1. The dog door opening must be at least 12” tall.
2. A button on the remote control opens the dog door
    1. if the door is closed, and closes the dog door if the door is open.
3. Once the dog door has opened, it should close automatically if the door isn’t already closed.

After creating the list, we validate requirements with the customer to make sure that we are all on the same level of understanding of what the system has to do. We can get approval in the best case, and also, we get some comments on the requirements list as a change needed.

Be aware that the happy case doesn't always happen in our real world, so our requirements might have an _alternative paths_ that handle the situation when things going wrong and unexpected.

The _Use case_ idiom describes _what your system does to accomplish a particular customer goal._ it provides one or more scenarios that convey how the system should interact with the end-user or another system to achieve a goal.

**One great use case is consists of 3 parts:**

| Part                     | Description                                                                                                        |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------- |
| Clear value              | The use case must have a clear value to our system, if it’s not then the use case isn't of much use                |
| Start and Stop Condition | Each use case mush have a defined starting and ending conditions. when to start and when the process must be ended |
| External Initiator       | Each use case is started by external actor outside the system                                                      |

The use case must be written in a clear language to be understandable for your customers, managers, and developers’ team. so that the use case doesn't have technical details.

You might think writing use cases is a waste of time and effort, but it's not what you think. Writing use cases helps you to figure out the edge cases and alternative paths that happens when things go wrong. By thinking about coding without take care of well written use cases we just think about happy scenarios only, the use case helps us to be aware of what we might face in the future. Remember that the first step of writing a great software is having satisfied customers.

## Check requirements against use cases

The last step is to check requirements against use cases, this helps us in validate the requirements and have the green light to start coding 🙂. here we make sure that all gathered requirements are covering all system aspects and functionalities.

---

# Chapter 03: Requirements Change

In this short chapter, the authors introduce the "**Change**" concept in the OOA&D world as it is the only constant. I agree with that change is the only constraint t in our world today.

well-designed use cases help us to implement our requirements after doing some changes easily and quickly as we don't need to worry about unexpected scenarios. so the authors advise us to use our use cases to find out about things our customers forget to tell us.

The steps of your main path in the use case list must be the steps that will happen **most often** in your project, others will be the alternative path. from the start step to the end, we call this path a **scenario**, Most use cases will have several scenarios but they always have the same user goal.

Any time we do changes to our use cases the requirements change too, so after any change, we need to go back to our requirements and check them again. _Change is constant, and your system should always improve every time you work on it._

---

# Chapter 04: Analysis

## Analysis

it is about figuring out potential problems, and then solving problems before you release your application out into the real world.

Analysis and your use cases let you show customers, managers, and other developers how your system works in a real world context not just in your controlled environment -**happy scenario**-.

**Delegation** shields your objects from implementation changes to other objects in your software. it protect our code from changes due to changes happening to other objects.

**Textual analysis** is about looking at _`nouns`_ in your use case to figure out _`potential classes`_, and _`methods`_.

Maybe You didn't use use cases and still create good software, but it's good to use them to satisfy your customers more often. and it's good to make sure your software does what it's supposed to do.

Pay attention to the nouns in your use case, even when they aren’t classes in your system, because textual analysis helps us with what to focus on, not just what classes you need. in some cases you will found nouns in your use case but it's not really needed to be a class in your system. such as in the following example:

![](https://github.com/0xGhazy/0xGhazy/assets/60070427/cba12cf2-a91f-4158-a2b8-f12d100be83c)

In this example we didn't need to create a `Dog` class because we don't need to track the dog we just need its bark sound, or it's not making sense to store the dog in the dog door -_at least for me :)_-, and finally the dog is an external factor from our system.

Pay attention to verbs in your use case, it's usually the methods of the class in your system.

## Class diagram

![](https://github.com/0xGhazy/0xGhazy/assets/60070427/a9741a47-72c6-47cb-808b-73763f682457)

The class diagram contains some information about relationships between classes and inner components such as data members and methods.

From the image above we can see that:

-   Solid lines from one class to another are called "association" it means that one class is associated with another class by reference, extension, inheritance, etc.
-   On that solid line we write the name of the attribute where the association takes place.
-   The number at the end of the line is the number of attributes, if it's 1 it's called `multiplicity`, otherwise it's called `unlimited` and it's denoted by `*`.

Class diagrams aren't everything because it has limited _type_ information we don't know the data structure that uses them if we have iterable objects is it List, ArrayList, Vector, or custom objects. Class diagrams also don't tell us about how to code our methods, it's only give us a 10,000-foot view of our system as what authors mention on page 187.

At the end of this chapter remember that **rewriting code takes a lot more time than rewriting a use case or redrawing a class diagram**

---

# Chapter 5: Good design = flexible software

In this chapter authors will revisit the change concept that as we mentioned above its the only constant in our world :). we will talk about how to make your software more flexible and reusable, apply OO principles to achieve cohesion, and more. . .

## Part 1: Nothing Ever Stays the Same

This part of Chapter 5 starts with "The harder you make it for your software to change, the more difficult it’s going to be to respond to your customer’s changing needs.". This part focuses on the change concept and how we can make it achievable by using some OOP techniques.

`Abstract classes` are placeholders for actual implementation classes. we use these classes to define common behaviors that are needed in the classes that will extend the abstract class.

We can't create abstract class instances so we use them in general objects such as in the mentioned example in the book on page 200.

![1123](https://github.com/0xGhazy/0xGhazy/assets/60070427/6e1a106f-0137-4bbe-b60f-ed9bdca222ea)

In this example we don't have an `Instrument` object in the real world it's just a placeholder for any kind of musical Instrument that we may need to add in the future.

_Whenever you find common behavior in two or more places, look to abstract that behavior into a class, and then reuse that behavior in the common classes_

Abstract classes in the class diagram are denoted as _ClassName_ in italics.

Aggregation relationship means that one thing is made up of another thing. In this case, an object adds another object, such as a parent object.

One of the best ways to see if the software is well-designed is to try and CHANGE it. trying to change your software will prove that your software is good or not based on the ability to change easily.

**Great software isn’t built in a day** as you working on the project you will always find something to improve, and many problems in design to solve.

Coding to an interface, rather than to an implementation, makes your software easier to extend.

![Screenshot 2023-06-08 182037](https://github.com/0xGhazy/0xGhazy/assets/60070427/73a6cd88-39ca-45c4-8e55-07b5eefe563f)

When you run into a choice like this, you should always favor coding to the interface, not the implementation.

By coding to an interface, your code will work with all of the interface’s subclasses even ones that haven’t been created yet. Instead of your code being able to work with only one specific subclass like `BaseballPlayer` you’re able to work with the more generic `Athlete`. That means that your code will work with any subclass of `Athlete`, like `HockeyPlayer` or `TennisPlayer`, and even subclasses that haven’t even been designed yet 🙂.

`Encapsulation` protect your classes from unnecessary changes.
_Anytime you have behavior in an application that you think is likely to change, you want to move that behavior away from parts of your application that probably won’t change very frequently. In other words, you should always try to encapsulate what varies._

Another thing to make your classes easy to change and not dependent is to have one reason to change, to achieve that you need to make your class do only one thing and do it well.

## Part 2: Give Your Software a 30-minute Workout

In this part, we will talk about how OO principles can really loosen up your application. And for the grand finale, you’ll see how higher cohesion can really help your coupling.

In this chapter, the authors changed the design in the first part after analyzing it and trying to apply what we learned in the first part of Encapsulation and others.

So you have to accept the idea of changing the design. Why didn't they do the correct design in the beginning? They wanted to prove that the design they showed you would be very good at a certain time, and it would not be easy for you to believe that it did not meet the purpose and needed modifications and additional work.

Design is iterative... and you have to be willing to change your own designs, as well as those that you inherit from other programmers.

Here we can feel the benefit of peer programming and that it helps us not to be completely impressed with our design, but there is criticism from the other side, which drives us to continuous development.

![p1](https://github.com/0xGhazy/0xGhazy/assets/60070427/dcefd364-5b76-4a3a-8897-43b123804b0e)

By encapsulating what varies, you make your application more flexible, and easier to change.

When you have a set of properties that vary across your objects, use a collection, like a `Map`, to store those properties dynamically.

You’ll remove lots of methods from your classes, and avoid having to change your code when new properties are added to your app

here we can use `Map<?>` instead of adding properties data members to the `InstrumentSpec` class.

The design will be like this:
![p2](https://github.com/0xGhazy/0xGhazy/assets/60070427/4a2188af-230e-4b8f-b01a-ae1bf3b5e366)

We can access the properties from the class:

```java
instrument.getSpec().getProperty("builder");
```

_Most good designs come from analysis of bad designs. Never be afraid to make mistakes and then change things around._

Now, we need to know about cohesion and cohesive class.

`cohesive class` _A cohesive class does one thing really well and does not try to do or be something else._

`Cohesion` _Measures the degree of connectivity among the elements of a single module, class, or object. The higher the cohesion of your software is, the more well-defined and related the responsibilities of each individual class in your application. Each class has a very specific set of closely related actions it performs._

It's about how closely related the functionality of a class is in an application, module, or object. cohesion adds reusability and is easy to change.

**The more cohesive your software is, the looser the coupling between classes.**

At the end of this chapter, I would like to end it with the part I liked the most in the chapter, which is the question of **when is the design good enough and stop developing and improving?**

_Sometimes you just have to stop designing because you run out of time... or money... and sometimes you just have to recognize you’ve done a good enough job to move on. Spending hours trying to write “`perfect software`” is a waste of time; spending lots of time writing great software and then moving on, is sure to win you more work, big promotions, and loads of cash and accolades_.

It's hard to know when to stop, but we can say in general if our software does what it is supposed to do, it has a flexible and cohesive design, and customers are happy with it. we will be ready to move on to a new project.

---

# Chapter 6: Solving really big problems

In this chapter we will talk about the introduction to building big applications, I really love this chapter. It makes me feel good and excited about reading it.

We start by introducing how to solve big problems, You solve big problems the same way you solve small problems. As the big problem is just a set of small problems. so we just divide the big problems into small functional pieces and deal with each piece individually.

Dealing with big problems doesn't really require special magic tools or information. we can use the concepts that we use to solve small problems such as Encapsulation, coding against interfaces, writing use cases, keep it simple and able to change easily.

We need a lot more information to understand what we want to build then we can start writing the requirement list and use cases. We can gain more information by determining what our system is like (commonality/similar) and What is the system not like (variability/different).

After figuring out what is our system like and what is not, we can figure out what are features of our system are, Features are just a high-level description of something a system needs to do. Features and requirements are the same thing for some people and are not for others. we can say features are “big things” that lots of requirements combine to satisfy. That's what I prefer.

Use cases don’t always help you see the big picture, We need to keep our attention to get the big picture only without unnecessary details for now. So we can start drawing the _Use Case Diagram_ we draw it when we need to know what a system does, but don’t want to get into all the detail that use cases require. here is an example of a use case diagram in the image below:

![image-2](https://github.com/0xGhazy/0xGhazy/assets/60070427/eba869ee-e38d-4d1b-b7fd-fd4537c2a14a)

A use case diagram is a blueprint for the system we wanna build, With a use case diagram, you’ll never forget about the big picture. identifying the features as we do before we can check them against the diagram to make sure it's complete.

Domain analysis lets you check your designs, and still speak the customer’s language, we’d never be sure we were building the right thing if we started talking about classes and variables. Here is an example of domain analysis:

![image-3](https://github.com/0xGhazy/0xGhazy/assets/60070427/7a2450b3-6d04-4ddc-b791-d42bf549862b)

**Domain Analysis**: The process of identifying, collecting, organizing, and representing the relevant information of a domain, based upon the study of existing systems and their development histories, knowledge captured from domain experts, underlying theory, and emerging technology within a domain.

Don’t forget who your customer really is, This is great advice at least for me. a lot of time I work on a project and get some thoughts about what if my customer is a developer. I need to add some features to make developers able to integrate my calculator into their systems 😃, I get a lot of work to do even if this project is small or big, it's maybe failed because additional features are not required for your real system users. Domain analysis helps you avoid building parts of a system that aren’t your job to build.

A design pattern is just a way to design the solution for a particular type of problem. So design patterns don’t go directly into your code, they first go into your BRAIN. we study them and learn how they were implemented and when to use them and when we can't use them, because each design pattern has its own trade-offs.

Our chapter is done here, I would like to document this moment right now. I was writing these chapter notes while I'm in the local cafeteria beside the Nile River and I asked for a coffee it was so bad but it cost 10 LE so it's fair 😁. See you in the next chapters.

---

# Chapter 7: Architecture

`Architecture` is the organizational structure of a system, including its decomposition into parts, its connectivity, interaction mechanisms, and the guiding principles and decisions that you use in the design of a system.

Architecture takes a big chaotic mess...and helps us turn it into a well-ordered application. if you didn't find where to start we can start with the features list and pick one feature but which one to start with? The things in your application that are really important are architecturally significant, and you should focus on them `FIRST`

To determine which feature is the most important, Ask yourself the following 3 questions:

1. **Is it part of the essence of the system?**
   If you can't imagine your system without this feature then it's a core part of your system.
2. **What does it mean?**
   If you don't really know what the description means, then it's probably pretty important to give some attention to this feature, anytime you think this part will take a lot of time or will create problems, start with it now rather than late.
3. **How do I do it?**
   Features that seem to be really hard to implement, or a totally new programming task for you, you better spend some time searching how it will be implemented, to not create lots of problems down the road.

The essence of a system is what that system is at its most basic level. Once you determine what are the most important parts to start with, you can start with any one of them. The point here is to reduce the risk so that we start with key features first.

Focus on one feature at a time to reduce risk in your project. Don’t get distracted by features that won’t help reduce risk.

Build on what you’ve already got done whenever possible. After finishing one feature picks the next one which depends on what you just finished before, this is good for your progress.

The more your design is good, the more risk will be reduced.

Sometimes the best way to write great code is to hold off on writing code as long as you can. Thinking and reevaluating your design is most important and helps you to write great code.

Customers don’t pay you for great code, they pay you for great software 😃.

---

# Chapter 8: Design Principles

In this chapter, the authors introduce a bunch of OO design principles, using proven OO Design results in more maintainable, flexible, and extensible software.

## Open-Closed principle (OCP)

In this principle your code must be closed for modification and open for extension.

![image](https://github.com/0xGhazy/0xGhazy/assets/60070427/20ab9521-61e7-4464-9a43-000b168bb354)

`InstrumentSpec` is closed for modification, The `matches()` method is defined in the base class and doesn’t change.

But it’s open for extension, because all of the subclasses can change the behavior of `matches()`

You can achieve this concept not only by extending another class, but if you have several private methods in a class, but those are also closed for modification no code can mess with them. But then you could add several public methods that invoked those private methods in different ways. this is considered an OCP.

OCP is a combination of encapsulation and abstraction.

## Don't Repeat Yourself principle (DRY)

Avoid duplicate code by abstracting out things that are common and placing those things in a single location.

We see the DRY principle at dog door implementation when putting the ability to close the door automatically inside the door class itself.

![image-1](https://github.com/0xGhazy/0xGhazy/assets/60070427/5739394e-ba74-45d8-ba43-a2edbb3cec21)

DRY is really about `ONE requirement` in `ONE place`. A requirement should be implemented one time, use cases shouldn’t have `overlap`, and your code shouldn’t repeat itself. DRY is about a lot more than just code.

## The Single Responsibility Principle (SRP)

Every object in your system should have a single responsibility, and all the object’s services should be focused on carrying out that single responsibility.

Cohesion is actually just another name for the SRP. If you’re writing highly cohesive software, then that means that you’re correctly applying the SRP.

|                 DRY                 |                           SRP                           |
| :---------------------------------: | :-----------------------------------------------------: |
| Put functions and data in one place | Make sure that your class does one thing and do it well |

The following image is a test to determine if your class applies or violates the SRP principle.

![image-2](https://github.com/0xGhazy/0xGhazy/assets/60070427/c3615624-c0f7-4921-bd88-f6306dacc5e7)

## The Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types.

The LSP is all about well-designed inheritance. When you inherit from a base class, you must be able to substitute your subclass for that base class without things going terribly wrong. Otherwise, you’ve used inheritance incorrectly!

Violating the LSP makes for confusing code, It’s hard to understand code that misuses inheritance.

Here are some inheritance alternatives.

### Delegate

when you hand over the responsibility for a particular task to another class or method.

Use delegation when you want to use another class’s functionality, as is, without changing that behavior at all.

### Composition

Composition allows you to use behavior from a family of other classes, and to change that behavior at runtime.

![image-3](https://github.com/0xGhazy/0xGhazy/assets/60070427/0f47c937-6c50-47aa-827b-0d6062343e1d)

In composition, the object composed of other behaviors owns those behaviors. When the object is destroyed, so are all of its behaviors.

The behaviors in composition do not exist outside of the composition itself.

### Aggregation

Aggregation is when one class is used as part of another class, but still exists outside of that other class.

![image-4](https://github.com/0xGhazy/0xGhazy/assets/60070427/344984fe-edf2-42d1-b708-ccba15dbe6f2)

If you favor delegation, composition, and aggregation over inheritance, your software will usually be more flexible, and easier to maintain, extend, and reuse.

The last thing in this chapter The LSP is not about sub classing, though, It’s about when to subclass.

---

# Chapter 9: Iterating and Testing

In this chapter, the authors introduce a bunch of different development approaches to design and implement our projects. Talking about testing our code, and making sure it works well as supposed.

Keep in mind that You write great software iteratively. We start with a general big picture and then go deeper into the solution until we complete it. as we go deeper into the solution our design decisions may be changed as we go deeper. Note that the design decisions are always tradeoffs 😃.

There are many approaches to developing an application, in this chapter we will spotlight two of them `Feature-driven development` and `Use case-driven development`.

|                                                                              Feature driven development `FDD`                                                                               |                                                                        Use case driven development `UCCD`                                                                        |
| :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| focus on specific features of the application. This approach is all about taking one piece of functionality that the customer wants, and working on that functionality until it’s complete. | focus on specific flows through the application. This approach takes a complete path through the application, with a clear start and end, and implements that path in your code. |
|                                                                                      Use Features list                                                                                      |                                                                                Use Use Cases list                                                                                |

In feature-driven development, we focus on one feature at a time, we can start with the feature that many features depend on it to

In the Use of case-driven development, we focus on one scenario at a time, starting with its start point, and going through its different paths till the end point.

Both of them are suitable for developing applications. So when to use `FDD` and `UCCD` -this is not a formal abbreviation I write them for short-?

| \*                                                             | Feature driven development | Use case driven development |
| :------------------------------------------------------------- | :------------------------: | :-------------------------: |
| Show the customer working code faster                          |             ✔              |             ❌              |
| User-centric                                                   |             ❌             |              ✔              |
| System has disconnected pieces of functionality                |             ✔              |             ❌              |
| Transactional systems                                          |             ❌             |              ✔              |
| Show the customer bigger pieces of functionality at each stage |             ❌             |              ✔              |

You should test your software for every possible usage you can think of. Be creative!
Don’t forget to test for `incorrect` usage of the software, too. You’ll catch errors early, and make your customers very happy.

Test cases make your customers happy because they got the job done, no matter how your code is clean as we mentioned before customers pay for great software. Test-driven development focuses on getting the behavior of your classes right.

Each time you iterate, reevaluate your design decisions and don’t be afraid to `CHANGE` something if it makes sense for your design. change always happens, so be sure you have the willing to change your design if needed.

|                                                                                                                     Programming by contract                                                                                                                     |                                                                                                                                      Defensive programming                                                                                                                                       |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| You and your software’s users are agreeing that your software will behave in a certain way. we assume that people using our code can handle `null` return values for example. we trust other coders and developers for being able to deal with such situations. | If we don't trust other developers and want to keep all safe, we throw an exception instead of a null value for accessing/getting not-existing values in a map or array. In this approach, our code will stop working when it hit any exception to 0make 0i0t safe for all users and developers. |

When you are programming by contract, you’re working with client code to agree on how you’ll handle problem situations.

When you’re programming defensively, you’re making sure the client gets a “safe” response, no matter what the client wants to have happen.

In Chapter 10, The authors recapped what they had mentioned in the past 9 chapters and tried to apply it to one project.

The end ❤
