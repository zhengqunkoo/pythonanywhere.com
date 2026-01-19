# Kubernetes Deployment Instructions

## Prerequisites
1. Ensure `kind` and `kubectl` are installed.
2. Ensure you have rebuilt your cluster with the updated config:
   ```bash
   kind delete cluster
   kind create cluster --config 2-workers-config.yaml
   ```

## Build and Load Image
Since the deployment uses a local image `flask-app:latest`, you need to build it and load it into the kind nodes.

1. Build the image:
   ```bash
   docker build -t flask-app:latest .
   ```

2. Load the image into kind:
   ```bash
   kind load docker-image flask-app:latest
   ```

## Deploy
Apply the manifests in this directory:
```bash
kubectl apply -f k8s/
```

## Access the App
Since we are using a NodePort service (or if you set up Ingress), you can access the app.
The simplest way to verify it works is to use `port-forward`:

```bash
kubectl port-forward service/flask-app-service 8080:80
```
Then visit `http://localhost:8080`.

If you want to use the mapped port 80 from the `2-workers-config.yaml`, you would typically install an Ingress Controller (like ingress-nginx) and create an Ingress resource.
