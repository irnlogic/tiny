# Deploying Tinurl app on Kubernetes

Push your docker images to a hub for use in Kubernetes cluster. 

## Push images to docker hub
### prequesites
* Register with https://hub.docker.com/
* On a command prompt run 'docker login', enter your credentials 

### push redis image
cd to directory tiny/dockercompose/redis

 ```
 docker build . -t <yourdockerhubusername>/redis:1.0
 docker push  <yourdockerhubusername>/redis:1.0
 ```
 
 ### push postgres image
cd to directory tiny/dockercompose/postgres

 ```
 docker build . -t <yourdockerhubusername>/postgres:1.0
 docker push  <yourdockerhubusername>/postgres:1.0
 ```
 
  ### push frontend image
cd to directory tiny/dockercompose/django

 ```
 docker build . -t <yourdockerhubusername>/djangotinyurl:1.0
 docker push  <yourdockerhubusername>/djangotinyurl:1.0
 ```
 
## Deploy in gcloud
Alternatively you may deploy in another Kubernetes cluster, where you have kubectl access!

### Prerequesites
Please be aware you may incur charges for use of Google Cloud. If you do not care to make your endpoint publically available / not interested in high scalability experiments etc at this time, [Minkube](https://kubernetes.io/docs/setup/learning-environment/minikube/), which can can run on your laptop is a good option.

* Register with <https://cloud.google.com> 
* Complete the 'Before you begin' section here ->  <https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app>. 
Make sure to activate and open the Google Cloud Shell. Skip Step 1, 2 etc!

* Create a Kubernetes cluster with 3 nodes
```
gcloud container clusters create tinyurl-cluster --num-nodes=3
```

If you are using another provider, please be sure you can run kubectl and have credentials to access your Kubernetes cluster

* On Google Cloud Shell, clone the repo so you have access to our Kubernetes deployment descriptors
```
git clone https://github.com/irnlogic/tiny.git
```
* cd into folder tiny/kubernetes

## deploy redis
```
 kubectl create -f redis-deployment.yaml
 kubectl create -f redis-service.yaml
```
## deploy postgres
```
 kubectl create -f postgres-deployment.yaml
 kubectl create -f postgres-service.yaml
```
## deploy frontend
```
 kubectl create -f frontend-deployment.yaml
 kubectl create -f frontend-service.yaml
```

Deployments and services will be created in a few minutes including a loadbalancer service for frontend.

Now list services you deployed in Kubernetes
```
kubectl get services
```

Among others you should see something like the following:
```
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
frontendxxxx   ClusterIP   11.11.345.22   191.51.245.21   8001/TCP
```

You should now be able start Tinuurl app ! -> http://EXTERNAL-IP:8001 (replace 'EXTERNAL-IP' with ip you get above)

Enjoy!
