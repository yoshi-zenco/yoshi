# Kubernetes Deployment Guide

## Prerequisites
- `kubectl` configured for your cluster
- `kustomize` v5+
- Container images pushed to GHCR

## Deploy to Staging

```bash
kubectl apply -k infra/k8s/overlays/staging
```

## Deploy to Production

```bash
kubectl apply -k infra/k8s/overlays/production
```

## Verify Deployment

```bash
kubectl get pods -n cleus
kubectl get ingress -n cleus
kubectl logs -f deploy/cleus-api -n cleus
```

## Rolling Update

```bash
kubectl set image deployment/cleus-api api=ghcr.io/cleus-ai/cleus-api:NEW_SHA -n cleus
kubectl rollout status deployment/cleus-api -n cleus
```

## Rollback

```bash
kubectl rollout undo deployment/cleus-api -n cleus
```
