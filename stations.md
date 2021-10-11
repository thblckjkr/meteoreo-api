# Creating a new instance of the project

Copy the environment file to a private one.

**DON'T FORGET TO CHANGE THE DEFAULTS**

```sh
cp .env.example .env
```

Creating a new private key to use to access the stations

```sh
ssh-keygen -t rsa -m PEM -f /app/private_key.pem
```
