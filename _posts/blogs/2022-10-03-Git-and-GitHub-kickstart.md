---
created: 2022-10-03
title: "Git and Github kickstart"
description: "A quick start guide to start using Git and Github the most famous version control system...."
layout: post
tags: [git]
category: [Blog]
image:
  path: https://www.biteinteractive.com/wp-content/uploads/2021/05/git-vs-github.png
  alt: Image from [Here](https://www.biteinteractive.com/wp-content/uploads/2021/05/git-vs-github.png)
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

Hello world, Hossam is here, welcome to my first blog in the Graduation Project Diary series, in this blog I try to explain and discuss new things that I have learned during the final year @ BFCAI ❤️.

3/10/2022 at 3:51 AM is the time I start to write this post, I start writing about Git and GitHub. why this topic? because the team needs to collaborate together during working on the project development, review each other’s tasks, create teams and assign tasks, track issues, and a lot of other useful features that improve productivity and quality. Get a cup of coffee, relax and let’s get started.

in this post, you will learn what is Git and GitHub and how to create a repository in your local machine and a remote one, how to push your code from the local repo to the remote one, creating branches, and how to switch from and to each other.

this post is not about how Git and GitHub work under the hood, I try to explain the basic idea and usage of Git, and GitHub as an entry-level that is enough to start using it and start a collaboration with your team.

## What is Git?

Git is a **distributed version control system**, which means that the entire codebase and history is available on every developer’s computer, which allows for easy branching and merging.

we use `Distributed` word because when we using git, every developer has his own copy of the project. not as the `Centralized` approach that you have a single “central” copy of your project on a server and commit your changes to this central copy. which leads to a lot of conflicts during working on the same project file.

as we mentioned earlier git is a **version control system**, in a simple words it's a _change tracker_ system, git helps us to detect any changes happened to our source code files, and give us the ability to commit this changes or revert them.

## Why Git?

Git is one of the most popular **version control system** worldwide, for many reasons such as:

- Git is Smart
  When we rename files, Git will not be confused with this action and it steals know that file didn't change it's just renamed.
- Git is Fast
- Git is Safe
  as mentioned above git give us the ability to commit/revoke our changes, it's very useful when we have do some mistakes and want to revoke them., or in the worst case scenario if a hacker pushes mal code to the project files we can revert changes made by him to keep our project and users safe.

## Git Downsides

- Git is not the best Choice for Handling Binary Files. binary files usually are big-sized so Git can't deal with these files at the same speed and quality as ASCII files (Source Code).
- Does not track empty folders

## What is GitHub?

GitHub is a for-profit company that offers a cloud-based Git repository hosting service.
we host our project repository (Project Folder) on GitHub to make the team able to access the project at any time and start collaboration.

![1](https://user-images.githubusercontent.com/60070427/195462450-53039943-1f57-45f8-b401-19288d9ae303.png)

now let's start with the practical part, in this part I suppose you have GitHub Account and Git Client on your machine, you can download Git Client from [here](https://git-scm.com/downloads).

Let's start with creating a new simple project.

```python
def add_two_numbers(number1: int, number2: int) -> int:
	"""Function to calculate the sum of two integer numbers"""
    return number1 + number2


if __name__ == '__main__':
    print("10 + 50 = ", add_two_numbers(10, 50))
```

I Create this simple console application in a directory called `calculator`

![2](https://user-images.githubusercontent.com/60070427/195462461-034825b7-7fe1-40c0-b526-c618d21ecb98.png)

we have a project now and we want to start tracking any changes that happened to the project files. so we need to init a new `repository`. first What is the repository?

Git repository is directory that saves the history of all changes made to the files in a Git project, it was a hidden directory called `.git`. once a directory initialized as a git repository we can start adding and tracking changes that happened. to init a new git repository we use `git init`

![3](https://user-images.githubusercontent.com/60070427/195462467-2fb7afeb-040c-4698-ba58-d314df370c5b.png)

as you can see I navigate to **/Desktop/Calculator** the path in which my project executes the git init command and now I have a git repository 😃.

let's see our repository status using the `git status` command.

![4](https://user-images.githubusercontent.com/60070427/195462469-01c539dc-a28e-42a9-bef4-1846659a3ef3.png)

git tells us that we have an Untracked file that we can add to the repository. by adding the files using `git add .` to add all files or `git add <file-name>` command. we will copy these files to the `staging area` which also called `the index`.

the staging area is an area between the working directory -project directory- and the git repository it self, for better understanding we can use the following image to explain it properly.

![5](https://user-images.githubusercontent.com/60070427/195462472-866757c7-852f-4b68-be5c-84bb12d36724.png)

First, we start in the working directory (project folder on your machine) which contains the project files this file is Untracked yet. when we wanna start tracking them we add them to the index or staging area, staging area is An intermediate place where modifications are made to the files and then these changes can be committed to the repository. Once we have committed changes to the repository, we have now a snapshot of the project files at this moment, then the working directory and the Repository are having the same file content.
Now we know what is the staging area, let's add our files to it to be tracked.

![6](https://user-images.githubusercontent.com/60070427/195462474-6e43c2f5-e97a-476b-8e1a-8999b29e8aeb.png)

I used the `git add <file>` command and then check the staging area status, and this time our file is tracked as we see in the previous picture.

if I wanna make mistake and want to unstage a staged file we can use the `git rm --cached <file>` command to revert the staging command for this file.

To take a snapshot of the staged file (move to the repository), we will use `git commit -m "Commit message"`. I'll commit the `example.py` file to the repository.

![7](https://user-images.githubusercontent.com/60070427/195462476-6682a4ed-36c9-43d0-ab13-46f01c2a0045.png)

After committing changes, our index/stage area is clean now. I use the `git log` command to display the repository history and the commits and now we can see the commit that we made a few seconds ago.

Assume we want to add a new feature to our great project, features that make our project so strong and trendy. Let's add our feature to the `example.py` file to be like the following

```python
def add_two_numbers(number1: int, number2: int) -> int:
    return number1 + number2

def sub_two_numbers(number1: int, number2: int) -> int:
    return number1 - number2

if __name__ == '__main__':
    print("10 + 50 = ", add_two_numbers(10, 50))
    print("50 - 20 = ", sub_two_numbers(50, 20))
```

![8](https://user-images.githubusercontent.com/60070427/195462479-5500d663-5711-4dcb-a864-c3140e82517c.png)

now we have added the new feature that makes us able to subtract two numbers, what a great job we do!

you may notice these words from the pictures above `On branch master`, what is branching at git?
branches/branching is a very important concept in git, in simple words, a branch is an independent line of development that has its own changes and history. to image and understand how branches work in git you can use the following image from git documentation

![9](https://user-images.githubusercontent.com/60070427/195462482-38ca037b-4334-4ad7-8ffd-fd05cfc9eff9.png)

the branch is a pointer that refers to commits at a specific moment of time, we can use it to create two independent versions of the same project -git is a version control system :)-, and the `HEAD`
is another pointer that refers to the currently used branch. let's create a new branch to demonstrate the idea, I'll create a premium version of this project that contains the multiplication and division features. let's start with creating a new branch called `premium` using the following command `git branch premium`

![10](https://user-images.githubusercontent.com/60070427/195462488-bc66b03f-18ea-48bf-b2e3-ebeb8033fca7.png)

using `git branch` to list all branches available in this repository, to delete a specific branch we use `git branch -d <branch-name>`, the green master branch is the currently used branch so let's switch to the premium branch using `git checkout premium`

![11](https://user-images.githubusercontent.com/60070427/195462492-bb88e247-5e27-4316-85c6-8eefc59df879.png)

i use cat command to display file content on the console screen, let's start adding our premium features to make the example.py file like this:

```python
def add_two_numbers(number1: int, number2: int) -> int:
    return number1 + number2

def sub_two_numbers(number1: int, number2: int) -> int:
    return number1 - number2

def multiply_two_numbers(number1: int, number2: int) -> int:
    return number1 * number2

def division_two_numbers(number1: int, number2: int) -> int:
    if number2 != 0:
        return number1//number2
    return "Second number can't be equals zero"


if __name__ == '__main__':
    print("10 + 50 = ", add_two_numbers(10, 50))
    print("50 - 20 = ", sub_two_numbers(50, 20))
    print("5 * 20 = ", multiply_two_numbers(5, 20))
    print("100 - 20 = ", division_two_numbers(100, 20))
```

![12](https://user-images.githubusercontent.com/60070427/195462497-04193e66-2fb3-463f-afca-da94d8790adf.png)

i have added the features and commit it to the repository under the premium branch, then i read the file to load it's content to you because you will see what happened when we try to checkout again to the master branch in the next image.

![13](https://user-images.githubusercontent.com/60070427/195462500-c266c71b-87c4-437d-aa8c-f1534761cead.png)

now as you can see the master branch steel in the free edition hasn't had the new features that we added above. but what happened under the hood?

using the `git checkout master` command do the following :

- Copy the committed changes by the master branch from the repository to the working directory.
- Then change the HEAD to the master branch
  what if I wanna change the branch without checkout files from the repository to the working directory? in this case we use the `switch` command `git switch master/premium`.

using the branching concept in git helps us to organize our work as a team prevent as conflicts as possible, we can create a branch for Fixing issues, features, design, documentation, and engineering...etc.

now let's talk about the last section in our post which in we will talk about how to push your code to the world, make your team contribute to it, and collaborate with each other.
we have to create a remote repository on GitHub using the `new` button

![14](https://user-images.githubusercontent.com/60070427/195462504-e1f07a70-dab2-4da0-88b0-d229d9c78be5.png)

![15](https://user-images.githubusercontent.com/60070427/195462506-bc973a31-4d23-4219-bf25-3fe7bbaaa9da.png)

I use `Calculator-Project` as a repository name and checked the `Add a README file` to put a project description if needed, then we click on the **create repository** button and now we have a remote repository on GitHub.

![16](https://user-images.githubusercontent.com/60070427/195462508-47adec0c-9b07-4a6c-9c84-51d6d8b56346.png)

now to push your code to the remote repository we click on the code button to get the remote repository link -make sure that you are in the HTTPS tab- like the image below.

![17](https://user-images.githubusercontent.com/60070427/195462515-37d83512-eec6-4317-badd-79106b422b76.png)

Let's back to our local terminal and add the remote repo to your project using the following command `git remote add origin <REMOTE URL>`

![18](https://user-images.githubusercontent.com/60070427/195462520-ef482147-a921-4893-b816-868248c3d1dc.png)

i use `git remote -v` command to verify the remote repository.

![19](https://user-images.githubusercontent.com/60070427/195462525-1a31203d-da14-455c-b7e6-62900f1afe87.png)

i use the `git push -u -f origin master` command to push my files from local machine to the remote machine on GitHub.

- `-u/--set-upstream` flag used to mark as an *upstream* reference. This allows you to later perform `git push` and `git pull` commands without having to specify an `origin` since we always want GitHub in this case.
- `-f/--force` This will automatically overwrite everything in the remote directory. We’re using it here to overwrite the default README that GitHub automatically initialized. this will remove the README.md file because it's not in our local machine repository.
  Your GitHub repository must be like this

![20](https://user-images.githubusercontent.com/60070427/195462527-1ad060dc-99d9-4aca-9bcf-b912a7a114bd.png)

now we have reached the end of this post talking about git, in the next part of this post I'll talk about how to collaborate as a team member, what is the pull request, merge, rebase, and how to deploy your git hub page as a documentation page and more 😃.

I hope this post was useful to you and helps you do well in your future projects, I try to be simple as possible and provide you the base knowledge you need to use Git and GitHub. I will be very happy if you contact me and tell me your opinion and point out any errors in the post via mail: hhamdypro@gmail.com
If you find this post useful, share it with your friends to spread the benefit among them.
Thank you for reading.

---

Refs:

- [Git Documentation](https://git-scm.com/doc)
- [Git Index - javatpoint](https://www.javatpoint.com/git-index)
- [3.1 Git Branching - Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [Git Branch](https://www.atlassian.com/git/tutorials/using-branches)
- [Adding locally hosted code to GitHub](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github)
- [How to Push an Existing Project to GitHub](https://www.digitalocean.com/community/tutorials/how-to-push-an-existing-project-to-github)
