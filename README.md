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

Per ChatGPT, you shouldn't use this as is:

The current implementation is relatively simple and not intended for production use. To improve the security of the code, consider the following suggestions:

Use an established SSH library: Consider using a well-established library like Cowrie (https://github.com/cowrie/cowrie) to create the SSH honeypot. Cowrie is an actively maintained SSH honeypot with advanced features and security measures built-in.

Rate-limiting: To prevent abuse, implement rate-limiting on the login attempts. This can help mitigate brute-force attacks and DDoS attempts.

Sanitize input data: Before storing data in the SQLite database, sanitize the user input (username and password) to prevent SQL injection attacks.

Use an ORM: Use an Object-Relational Mapping (ORM) library like SQLAlchemy for better database handling, abstraction, and security.

Use HTTPS: Use HTTPS for the web server to encrypt the data in transit. This can be done using Flask and Let's Encrypt for free SSL certificates.

Secure Flask app: Follow Flask's deployment best practices for securing your web application, like setting a strong secret key, using the 'safe' filter in Jinja2 templates, and using a reverse proxy with a production-ready WSGI server like Gunicorn (https://flask.palletsprojects.com/en/2.1.x/deploying/gunicorn/).

Authentication: Add an authentication layer to the web server to protect the login attempts data from unauthorized access.

Separate sensitive data: Do not store sensitive data like private keys in the same directory as the code. Instead, use environment variables or configuration files to store sensitive information.

Update dependencies: Regularly update the dependencies (e.g., Paramiko, Flask) to ensure you have the latest security patches.

Logging: Implement proper logging to monitor the honeypot's activity and detect potential issues.

Keep in mind that creating a secure honeypot requires a deep understanding of security best practices and potential attack vectors. Always thoroughly test and review the security of your code before deploying it in a production environment.
