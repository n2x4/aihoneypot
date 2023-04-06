# aihoneypot
SSH Honeypot written by ChatGPT

!!WARNING!! Use at your own risk. The code works, but I make no guarantees that the code is secure in any form !!WARNING!!

I wanted to build a honeypot that would log SSH attempts and show those attemts and the credentials used on a webpage so I spent some time with GPT4 building something that would work.

Per ChatGPT: This SSH honeypot is using the paramiko library for SSH handling, the sqlite3 library for database interactions, and the Flask library for the web server. Please make sure to take necessary precautions while working with real-world SSH connections.

First, install required libraries:

pip install paramiko Flask

Then run the SSH Honeypot and the webserver:
python3 ssh_honeypot.py &
python3 webserver.py

Once those two are started, visit http://yourip:5000 and wait for any SSH attempts to yourip:2222 (port 2222). 

You may want to remap the ports to run elsewhere (such as port 80 for the webserver and port 22 for the honeypot). Just remember to move the real SSH port before you do this.
