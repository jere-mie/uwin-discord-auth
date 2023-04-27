# uwin-discord-auth

A web interface to authenticate UWindsor students and add them to a Discord server

*Note* Setup for this application is probably going to take a non-small amount of work. If you're reading this now, I definitely need to write a whole lot more documentation, so tread lightly

## Setup

### SSL Certs

SSL certs are required for localhost when running this application locally. You can create them with the following command:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
