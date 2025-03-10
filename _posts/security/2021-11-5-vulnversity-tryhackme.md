---
created: 2021-11-05
title: "Vulnversity | TryHackMe"
description: "My Writeup for Vulnversity machine from TryHackMe"
layout: post
tags: [TryHackMe]
category: [Cybersecurity]
image:
    path: /assets/img/security/vulnversity.png
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

Hi folks in this simple writeup I'll explain the steps that I followed to solve the Vulnversity machine on the TryHackMe, I hope you benefit from it and don't get bored of it, and if so, this is my first try bro 😥.

before we start we need to check some requests to make sure we are able to connect to the TryHackMe network. I recommend that you pass the OpenVPN room to be able to connect to the private network on which the target machine is located.

# [Task 01] Deploy the machine

In this simple easy task, you just need to click on the green button "Start Machine" to start the vulnerable machine to make it accessible to us.

As soon as the machine's IP address appears in the machine description box, you can deal with it immediately and start working on what is required of you in each task.

![](https://0xghazy.files.wordpress.com/2021/11/machine_info.png?w=1024)

Using the ping command, I make sure that I am connected to the machine and that it responds to the ICMP requests that I send to it.

![](https://0xghazy.files.wordpress.com/2021/11/check_connectivity.png?w=691)

As it appears in the picture above, the machine responds to us, which means that we are connected and this is good, so we can complete the task easily.

![](https://0xghazy.files.wordpress.com/2021/11/mission1.png?w=1024)

# [Task 02] Reconnaissance

In this task, we will use Nmap for scanning our target machine and collect information can be collected that may be useful to us in our pen testing process. TryHackMe gives you some useful switches you can use as you want to check what is required.

## 1- Scan the box, how many ports are open?

I used -sV switch to perform a Version scan to know how many TCP ports are open on this machine and what services run on it.

![](https://0xghazy.files.wordpress.com/2021/11/service-scan.png?w=816)

By looking at this result we now know how many ports are open.

![](https://0xghazy.files.wordpress.com/2021/11/m1.png?w=1024)

## 2- What version of the squid proxy is running on the machine?

from the previous photo, we can notice that the squid proxy runs on port 3128 and its version is 3.5.12.

![](https://0xghazy.files.wordpress.com/2021/11/m2.png?w=1024)

## 3- How many ports will Nmap scan if the flag -p-400 was used?

by using -p switch we can scan a specific port number but when we use -p-<port> we scan for a port range so by using -p-400 we are scanning for 400 port <1-400>

![](https://0xghazy.files.wordpress.com/2021/11/m3.png?w=1024)

## 4- Using the nmap flag -n what will it not resolve?

In this task, I thought I should try this switch and I would get an error message in the results but from the man page I found that it only asks you to see which protocols it can't resolve by using this switch.

![](https://0xghazy.files.wordpress.com/2021/11/nmap-man.png?w=617)

![](https://0xghazy.files.wordpress.com/2021/11/m4.png?w=1024)

## 5- What is the most likely operating system this machine is running?

we can use -A switch to try to know what operating system is running on the target machine, but from result @ -2 we know that the target runs a unix/linux kernel and the Apache server is running on ubuntu. We conclude from this that most of the possibilities indicate that it is the Ubuntu system.

![](https://0xghazy.files.wordpress.com/2021/11/os-detection.png?w=867)

![](https://0xghazy.files.wordpress.com/2021/11/m5.png?w=1024)

## 6- What port is the web server running on?

from 2 we know that Apache web server running on a 3333 port

![](https://0xghazy.files.wordpress.com/2021/11/m6.png?w=1024)

Since there is a web server on this machine, then I can browse it from the browser, which will be addressed as http://10.10.45.252:3333

![](https://0xghazy.files.wordpress.com/2021/11/home_page.png?w=1024)

_[7/Note] It's important to ensure you are always doing your reconnaissance thoroughly before progressing. Knowing all open services (which can all be points of exploitation) is very important, don't forget that ports on a higher range might be open so always scan ports after 1000 (even if you leave scanning in the background)_

# [Task 03] Locating directories using GoBuster

GoBuster is a tool used to brute-force URIs (directories and files), DNS subdomains, and virtual host names. For this machine, we will focus on using it to brute-force directories.

Download GoBuster [here](https://github.com/OJ/gobuster), or if you're on Kali Linux 2020.1+ run sudo apt-get install gobuster

![](https://0xghazy.files.wordpress.com/2021/11/99999999999999.png?w=1024)

If you are using Kali Linux you can find many wordlists under **/usr/share/wordlists**. but in my case, i used a list consist more common directories to perform the process faster. you can get it from here.

![](https://0xghazy.files.wordpress.com/2021/11/go1.png?w=767)

By viewing these existing directories that we found from the previous scan, we will find that there is a page to upload files on the server under the name /internal/index.php

![](https://0xghazy.files.wordpress.com/2021/11/m1-1.png?w=1024)

I have tried uploading a text file and a simple PHP file, but the result is that it rejected all of these formats

![](https://0xghazy.files.wordpress.com/2021/11/invalid_ext.png?w=851)

# [Task 04] Compromise the web server

Since the file upload page is in PHP format, if it is very obvious, the filter will reject any php file because in this need it is executable as a shell file, for example, so it will always be the rejected format

![](https://0xghazy.files.wordpress.com/2021/11/m1-2.png?w=1024)

then I created a simple word list of common php formats as in the task description:

![](https://0xghazy.files.wordpress.com/2021/11/screenshot_2021-11-06_11-33-20.png?w=408)

As recommended in the task description above, I will be using the burp suite tool to perform brute forcing to upload these files to see which of them are acceptable from this filter.

Instead of configuring your browser to deal with the proxy server of the Burp Suite tool, you can use the browser extension "FoxProxy" to do this automatically, and you can see this [article](https://blog.nvisium.com/setting-up-burpsuite-with-firefox-and) to learn how to do that.

After configuring the extension to the browser, I made an attempt to upload a file to the server, and I received the request to upload it to the proxy of theBurp Suite, and then I send it to the intruder tab.

![](https://0xghazy.files.wordpress.com/2021/11/proxy.png?w=991)

in the intruder tab especially in "Position" we can modify request content as we want so I try to change the extension only by adding  "§" around the extension name to be as same as the second photo below.

![](https://0xghazy.files.wordpress.com/2021/11/intruder.png?w=999)

![](https://0xghazy.files.wordpress.com/2021/11/req.png?w=520)

then we go to the "Payloads" tab to load our extensions file which we create before or you can insert it manually. after that, we can click on start attack and "Let the magic begin" 😎

![](https://0xghazy.files.wordpress.com/2021/11/payloads.png?w=684)

We will find that the "phtml" extensions with state Success.

![](https://0xghazy.files.wordpress.com/2021/11/response.png?w=940)

Then I go to this link to download the PHP-reverse-shell. by clicking on the "Raw" button to be able to display the code as a raw string then clicking right-click and saving the page as "shell.phtml". After that, you can upload it to the server.

![](https://0xghazy.files.wordpress.com/2021/11/shell_github.png?w=1024)

after downloading it we need to change the IP address to our ip address to receive all incoming connections, you can get your IP address from: http://10.10.10.10

![](https://0xghazy.files.wordpress.com/2021/11/change-ip.png?w=575)

![](https://media0.giphy.com/media/S79NL9AGw9Cye65fhn/giphy.gif)

In fact, now we are supposed to have uploaded the file to the server, but we do not know where the uploaded files are, so we will go back to using the GoBuster tool again at the address in the image and from it we find that it is on the path /uploads/

![](https://0xghazy.files.wordpress.com/2021/11/gobuster2.png?w=891)

And now we can listen to the incoming connections using the "Net Cat" tool

![](https://0xghazy.files.wordpress.com/2021/11/listening.png?w=638)

Now by going to the uploads directory, we can find our shell there

![](https://0xghazy.files.wordpress.com/2021/11/uploads-directory.png?w=794)

By clicking on our shell we will get a shell session immediately from the target machine, and we can make sure of that by seeing the result of pressing it from a tool

![](https://0xghazy.files.wordpress.com/2021/11/hacked.png?w=1002)

to get the username of this machine we can go to /home to know the username of the person who manages the web server.

![](https://0xghazy.files.wordpress.com/2021/11/username.png?w=527)

![](https://0xghazy.files.wordpress.com/2021/11/m3-2.png?w=1024)

By navigating to bill and reading the txt file there we will see the user flag

![](https://0xghazy.files.wordpress.com/2021/11/user-flag.png?w=557)

![](https://0xghazy.files.wordpress.com/2021/11/m4-1.png?w=1024)

![](https://media1.giphy.com/media/iKBAAfYNDu1dowhnEj/200.webp?cid=ecf05e4750by0hk8ne9nc07c8lx53nk30k4h0wf3ey50zfmx&rid=200.webp&ct=g)

# [Task 05] Privilege Escalation

From the description of the task on the website, you can tell that the solution here lies in SUID permissions, Here is an article that talks about it in some detail: https://www.redhat.com/sysadmin/suid-sgid-sticky-bit

we want to get all files that have this kind of permission so i will use the find command, for more information about this command you can join a free room Find, or use the command in Hint (not recommended 😃)

![](https://0xghazy.files.wordpress.com/2021/11/perm.png?w=1024)

After searching, we found some files that allow us to use it via SUID permissions. After searching a little on Google for any information on anyway to use them to escalate our privileges. Indeed, I found that the /bin/systemctl file is the appropriate one, and on it, I can do what is required.

![](https://0xghazy.files.wordpress.com/2021/11/screenshot-2021-11-06-182830.png?w=1024)

![](https://0xghazy.files.wordpress.com/2021/11/screenshot-2021-11-06-182851.png?w=922)

![](https://0xghazy.files.wordpress.com/2021/11/m1-3.png?w=1024)

we will use the SUID script above and modify it a little bit, to copy the content /root/root.txt to another Txt file.

![](https://0xghazy.files.wordpress.com/2021/11/script.png?w=801)

and now the final step is to read the "/home/bill/final_output.txt" 😃

![](https://0xghazy.files.wordpress.com/2021/11/final.png?w=684)

![](https://0xghazy.files.wordpress.com/2021/11/m2-2.png?w=1024)

Thus, we will be able to hack the Vulnversity machine from TryHackMe. I hope that you have benefited from this write-up. If you like it, let me know in the comments, and help me spread it by sharing it with those who are interested. Thank you for reading, See you in another writeup, my friend. salaam 💙
