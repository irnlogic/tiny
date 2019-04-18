# Scalable 'Tiny url' app example
This is a project to demonstrate deployment and scaling of the famous tiny url app using kubernetes.
Project can be run and tested on your laptop with docker-compose and  be deployed on kubernetes without code modification

Tiny url app is often used as an exemplary application to demonstrate various aspects of software scaling due its simplicity. Essentially it has following featureset:
- Given a long url, convert it to a short url
- Given short url, return the original url

Thats it, however please do not underestimate the challnge here, you can still run into all of the bottlenecks that you would see in any or more 'complex' application :)

Our Tiny app application will be made out of 3 services:
- Django rest server
- Redis cache
- Postgres database

The Django rest server will orchestrate redis and postgres to perform its functions
