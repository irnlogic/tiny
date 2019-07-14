# Deploying Tinurl app on Kubernetes

## Push your docker images to docker hub for use in Kubernetes 
### Prerequesites
* Register with https://hub.docker.com/
* On a command prompt run 'docker login', enter your credentials 

### push redis image
cd into directory tiny/dockercompose/redis
Build and then push image to docker hub like so
 ```
 docker build . -t <yourdockerhubusername>/redis:1.0
 docker push  <yourdockerhubusername>/redis:1.0
 ```
 
 ### push postgres image
cd into directory tiny/dockercompose/postgres

 ```
 docker build . -t <yourdockerhubusername>/postgres:1.0
 docker push  <yourdockerhubusername>/postgres:1.0
 ```
 
  ### push frontend image
cd into directory tiny/dockercompose/django

 ```
 docker build . -t <yourdockerhubusername>/djangotinyurl:1.0
 docker push  <yourdockerhubusername>/djangotinyurl:1.0
 ```
 
## Deploy in Google Cloud Kubernetes
Alternatively you may deploy in another Kubernetes cluster, where you have [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) access!

### Prerequesites
Please be aware you may incur charges for use of Google Cloud. If you do not care to make your endpoint publically available / run scalability experiments at this time, [Minkube](https://kubernetes.io/docs/setup/learning-environment/minikube/), which can run in your laptop is a good option.

* Register with <https://cloud.google.com> 
* Complete the 'Before you begin' section here ->  <https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app>. 
Make sure to activate and open the Google Cloud Shell. Skip Step 1, 2 etc!

* Create a Kubernetes cluster with 3 nodes
Zone below is chosen as 'us-west1-b', please choose a zone in your geographic vicinity 
```
gcloud container clusters create tinyurl-cluster --num-nodes=3 --zone=us-west1-b
```
You should see something like after success
```
NAME             LOCATION    MASTER_VERSION  MASTER_IP      MACHINE_TYPE   NODE_VERSION   NUM_NODES  STATUS
tinyurl-cluster  us-west1-b  1.12.8-gke.10   34.83.105.229  n1-standard-1  1.12.8-gke.10  3          RUNNING
```
If you are using another provider, please be sure you can run kubectl and have credentials to access your Kubernetes cluster

* On Google Cloud Shell, clone the repo so you have access to our Kubernetes deployment descriptors
```
git clone https://github.com/irnlogic/tiny.git
```
* cd into folder tiny/kubernetes
```
cd tiny/kubernetes
```
Replace the docker image names in the 3 deployment descriptors (xxxx-deployment.yaml files) before running commands below. 
e.g. replace 'rnlogic/postgres' with '<yourdockerhubusername>/postgres'
## deploy redis
```
 kubectl create -f redis-deployment.yaml
 kubectl create -f redis-service.yaml
```
## deploy postgres
```
 kubectl create -f postgres-configmap.yaml
 kubectl create -f postgres-deployment.yaml
 kubectl create -f postgres-service.yaml
```
## deploy frontend
```
 kubectl create -f frontend-deployment.yaml
 kubectl create -f frontend-service.yaml
```

Deployments and services will be created in a few minutes including a loadbalancer service, which exposes Tinurl frontend to public internet.

Now list services you deployed in Kubernetes
```
kubectl get services
```

Among others you should see something like the following:
```
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
frontend     LoadBalancer   10.38.14.217   33.230.6.53   8001:30080/TCP   58s
kubernetes   ClusterIP      10.98.2.1      <none>        443/TCP          12m
postgres     ClusterIP      10.98.8.269    <none>        5432/TCP         2m8s
redis        ClusterIP      10.96.11.24    <none>        6379/TCP         3m57s
```

You should now be able start the Tinyurl app using public IP ! -> http://EXTERNAL-IP:8001 (replace 'EXTERNAL-IP' with ip you get above)

