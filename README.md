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
```

Wait 3 minutes and the cluster should be bootstrapped.
