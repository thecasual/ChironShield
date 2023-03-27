<h1 align="center">
Chiron Shield
</h1>

<h3 align="center">
Proof of concept Semgrep + ChatGPT integration
</h3>

![Alt text](/img/Chiron-Shield.png )

Image credit to DALL-E

Prompt: Futuristic Chiron Shield, pixel art, cyber security


```
usage: run.py [-h] [-t] [-f F]

ChironShield

optional arguments:
  -h, --help  show this help message and exit
  -t          Test Sample files
  -f          file
```


### Example

```
python3 run.py -f samples/sqli1.py
```

```
########################################
File path: samples/sqli1.py

Semgrep ID:
python.sqlalchemy.security.sqlalchemy-execute-raw-query.sqlalchemy-execute-raw-query

Impact: HIGH

Vulnerable code:
mycursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")

Semgrep recommendation:
Avoiding SQL string concatenation: untrusted input concatenated with raw SQL query can result in SQL Injection. In order to execute raw query safely, prepared statement should be used. SQLAlchemy provides TextualSQL to easily used prepared statement with named parameters. For complex SQL composition, use SQL Expression Language or Schema Definition Language. In most cases, SQLAlchemy ORM will be a better option.

ChatGPT recommended fix:
mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

CWE:
CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

OWASP:
A01:2017 - Injection
A03:2021 - Injection

########################################
```

Disclaimer:

The code provided is for educational and informational purposes only. The creator of this code is not responsible for any consequences that may arise from its use. The user assumes all responsibility and liability for the use of this code. It is the user's responsibility to ensure that the code is used in a lawful and ethical manner.