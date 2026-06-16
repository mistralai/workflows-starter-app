---
id: diagnostics
title: Diagnostics
sidebar_position: 21
---

# Diagnostics: wf-diagnose

`wf-diagnose` is a CLI command that prints a self-contained diagnostic report for support triage. It covers system info, installed package versions, worker env vars, full parsed config, plugins, `/whoami` response, and connectivity checks against the Mistral API and the execution engine.

## Running Locally

```bash
wf-diagnose
```

Or via module:

```bash
python -m mistralai.workflows.scripts.diagnose
```

## Running on a Kubernetes Cluster

### Step 1 — Confirm Cluster Context

```bash
kubectl config current-context
```

Verify this points to the correct cluster (dev/prod).

### Step 2 — Find Worker Pods

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/name=mistral-workflows-worker --no-headers
```

Pick a running workflows worker pod.

### Step 3 — Check if wf-diagnose Exists in the Pod

```bash
kubectl exec -n <namespace> <pod> -c worker -- uv run python -c \
  "from mistralai.workflows.scripts.diagnose import main; print('found')"
```

- If `found` is printed, skip to Step 5.
- If `ModuleNotFoundError`, the deployed SDK version predates `wf-diagnose`. Proceed to Step 4.

The `-c worker` flag selects the worker container. Pods may have init containers; omitting it may exec into the wrong one.

### Step 4 — Copy diagnose.py to the Pod

The pod filesystem is typically read-only, so copy to `/tmp`:

```bash
kubectl cp \
  workflow_sdk/mistralai/workflows/scripts/diagnose.py \
  <namespace>/<pod>:/tmp/diagnose.py \
  -c worker
```

Adjust the source path to wherever the `workflow_sdk` checkout lives locally.

### Step 5 — Run the Diagnostic

If `wf-diagnose` is available natively (Step 3 succeeded):

```bash
kubectl exec -n <namespace> <pod> -c worker -- uv run wf-diagnose
```

If copied to `/tmp` (Step 4):

```bash
kubectl exec -n <namespace> <pod> -c worker -- uv run python /tmp/diagnose.py
```

Use a timeout of at least 30 seconds — connectivity checks can be slow.

## Troubleshooting

### `tar: Cannot open: Read-only file system`
The pod has a read-only root filesystem. Always copy to `/tmp`, not to the site-packages directory.

### `No such container: worker`
List containers with:
```bash
kubectl get pod <pod> -n <namespace> -o jsonpath='{.spec.containers[*].name}'
```
