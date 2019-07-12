
Push your docker images to a hub for use in Kubernetes cluster or other purpose. 

# Push images to docker hub
## prequesites
* Register with https://hub.docker.com/
* On a command prompt run 'docker login', enter your credentials 

## push redis image
cd to directory tiny/dockercompose/redis

 ```
 docker build . -t <yourdockerhubusername>/redis:1.0
 docker push  <yourdockerhubusername>/redis:1.0
 ```
 
 ## push postgres image
cd to directory tiny/dockercompose/postgres

 ```
 docker build . -t <yourdockerhubusername>/postgres:1.0
 docker push  <yourdockerhubusername>/postgres:1.0
 ```
 
  ## push frontend image
cd to directory tiny/dockercompose/django

 ```
 docker build . -t <yourdockerhubusername>/djangotinyurl:1.0
 docker push  <yourdockerhubusername>/djangotinyurl:1.0
 ```
 
