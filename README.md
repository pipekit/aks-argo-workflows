# aks-argo-workflows

## Bootstrapping a cluster
This is a public git repo, so you just need to get argocd installed into the cluster. Argocd will then connect to this repo and will deploy the rest after a few minutes.

Ensure the cluster you wish to bootstrap is in your kubectl context:

```bash
kubectl config current-context
```

The following commands may break your cluster if you have existing data in there:
```bash
kubectl create namespace argocd
kustomize build argocd | kubectl apply -f -
sleep 5
kustomize build argocd | kubectl apply -f -
```

We run the kustomize command twice to ensure that the CRDs are created before any CRs are applied.

Wait 3 minutes and the cluster should be bootstrapped.

## Running the workflow

Whilst you have the cluster as your current one in kubectl, with `workflows` as the default namespace you can run `make` to build the images, install the WorkflowTemplates and run the workflow. You can do this again to run it again, building anything that has changed in the mean time.

This will build 4 docker images, and will base them on `python:3.13` as the base image, swap that out if you want to for one that is suitable. It will push the resulting images to a repository set by the environment variable "DOCKER_REPO" which you can set with `DOCKER_REPO=myprivate.com/repo make`. If this requires authentication to push to, you must login first. You will then have to modify any instances of `joibel` in the yaml to match this location manually. Your cluster must already be able to pull from this location.
