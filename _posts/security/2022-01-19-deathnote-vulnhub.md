---
created: 2022-01-19
title: "DEATHNOTE Box | VulnHub"
description: "My Writeup for DEATHNOTE Box from VulnHub"
layout: post
tags: [VulnHub]
category: [Cybersecurity]
image:
    path: /assets/img/security/deathnote.png
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

Hi folks. Hossam Hamdy aka 0xGhazy is here, Today I'll explain how I PWN DeathNote machine from VulnHub

# [#] About the machine

Name: Deathnote: 1
Date release: 4 Sep 2021
Author: HWKDS
Series: Deathnote
Filename: Deathnote.ova
File size: 658 MB
MD5: D5F6A19BBEA617D7C7C46E21C518F698
SHA1: BDAAB12DE17BB6696ECA324A0BB4027B62D44A49

# [#] Machine enumeration

After starting our machine we can type this command to get all live hosts in our network

```bash
sudo netdiscover -r 10.0.0.0/24
```

![](https://user-images.githubusercontent.com/60070427/151669759-46656529-1dee-4a3f-aa66-c814055ba392.png)

Deathnote IP address is: `192.168.1.5`

## 1- Nmap enumeration

by running this command

```bash
nmap -sC-sV 192.168.1.5
```

![](https://user-images.githubusercontent.com/60070427/151669909-564022f8-1f22-4238-a625-47c3a7ef6e76.png)

we found that we have SSH on port 22, and web server at port 80 but there was a redirection so we need to append this address to our /etc/hosts file by using this command sudo echo "192.168.1.5 deathnote.vuln" >> /etc/hosts

## 2- Site enumeration

By visiting http://deathnote.vuln/wordpress

![](https://user-images.githubusercontent.com/60070427/151670235-886e89bc-7402-4505-b10c-372f89acac93.png)

![](https://user-images.githubusercontent.com/60070427/151670250-03e23ec7-fe33-48ba-8c93-e14250c5f502.png)

We have 3 interesting text [`Kira`, `L`] it seems to be a usernames and the last one is "iamjustic3" seems to be a password like passwords in CTFs :)

_From Hint: we need to find file called notes.txt_

## 3- Gobuster enumeration

I used this command to enum the web server gobuster dir -u http://deathnote.vuln/wordpress -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

![](https://user-images.githubusercontent.com/60070427/151670432-52923816-c7c1-435e-80d1-d8f6109b7049.png)

I found this admin directory wp-admin and it contains a login page.

by visiting the rest two directories didn't find something useful. so i go to read robots.txt file

by looking at `robots.txt` file we get this message :)

```
fuck it my dad
added hint on /important.jpg
ryuk please delete it
```

seems we have a new potential username here: `ryuk`

by cURLing the /important.jpg file we get this important information

![](https://user-images.githubusercontent.com/60070427/151670819-19586c48-6207-4ec0-9834-bd3341228ff2.png)

now we can log in to the WordPress CP. I try with "user.txt" and "iamjustic3" it files every time. i released that page title login Kira so i use kira as an username and it success this time :)

![](https://user-images.githubusercontent.com/60070427/151671005-1b4c308e-cbe0-461c-af53-5572654a6c4b.png)

Pingo we are in 🎉😎

by viewing posts, and pages we found nothing useful but in media, I found `notes.txt` file and read it, it seems to be a word list for something. since we have a user and password for WordPress, I think it will be an SSH credential.

![](https://user-images.githubusercontent.com/60070427/151671014-39483d61-701f-433d-ade4-71bfa8dc36c0.png)

# [#] Password Cracking

we have potential users such as `Kira` and `L` so we need to attempt to get a valid password for a valid username.
I want to write my own Python script but thinking about "why do I want to invent the wheel?". But found that there was well-known existing tool by searching about "SSH password cracking" and i found this useful article

I used this command hydra -l l -P wordlist.txt ssh://192.168.1.5
After using this command I find that only l have a valid password

![](https://user-images.githubusercontent.com/60070427/151671537-02f0870e-4b5c-41b4-bf4b-603dd9092ddc.png)

# [#] Gaining access

lets try to connect with SSH using this command ssh l@192.168.1.5 We get a connection but can't find any sudo command can i run to escalate.

![](https://user-images.githubusercontent.com/60070427/151671743-9c5cfa7d-f3f9-47c7-9750-635263c42889.png)

So I try to find a new way. after a while, I find a notification in the plugin module. after some searching, I find that the "Hello Dolly" plugin has an exploit. searching for the shell I find that I can edit the plugin PHP code == reversed shell :).

Getting PHP reversed shell from pentester monkey, And updating plugin source code.
![](https://user-images.githubusercontent.com/60070427/151671923-cce49703-1ebe-4dc1-88d3-deb5e396eb01.png)

Now let's go and access the plugin from this link: http://deathnote.vuln/wordpress/wp-content/plugins/hello.php

Let's setup our listener using NetCat using this command

```bash
nc -nlvp 4444
```

![](https://user-images.githubusercontent.com/60070427/151671934-2f8a06b8-4647-4300-941e-5ec2d6753960.png)

After getting connection successfully, We can enhance our shell using python3 -c 'import pty;pty.spawn("/bin/bash")'

After that, i stuck for a while, didn't know where I go after that. So I try to find a hint.txt or user.txt or flag.txt using this command `find / -type f -name hint/user/flag`

![](https://user-images.githubusercontent.com/60070427/151672119-ea916101-2c5e-459e-b3bd-bd36860db9b7.png)

I have the permission to visit /opt/L the directory, So let's see what is there.

![](https://user-images.githubusercontent.com/60070427/151672119-ea916101-2c5e-459e-b3bd-bd36860db9b7.png)

I have the permission to visit /opt/L the directory, So let's see what is there.

![](https://user-images.githubusercontent.com/60070427/151672253-cf2067bd-3650-425c-a92a-97fdab9eef6b.png)

Now I need to navigate to /fake-notebook-rule and view what is there!

![](https://user-images.githubusercontent.com/60070427/151672256-25b07b86-36c2-4ceb-9964-2e72a1983f96.png)

Let's go to `Cyberchef` and know what this Hex text means.

![](https://user-images.githubusercontent.com/60070427/151672384-a035fddb-544d-49c6-a6aa-98f937991792.png)

Password is: `kiraisevil`, Now I can log in with Kira account username and see what sudo permissions she has.

![](https://user-images.githubusercontent.com/60070427/151672509-4cdd7630-b312-4b13-b8c1-85a49bed3561.png)

Now we have root access on the Deathnote machine and that's what we want 😃.

What i have learned?

- "Hello, Dolly" is a vulnerable WordPress plugin.
- Using Hydra for cracking SSH login.
- The person who reviewed this article before publishing it is the cutest person ever 😀❤.
