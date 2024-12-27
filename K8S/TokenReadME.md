### <div style="text-align:center;color:green;">Creating a Token & Token Validity</div>

1. Create a token with default expiration (1 hour):

```bash
kubectl create token all-ns-user
```

2. Create a token with custom expiration:

For 5 hours

```bash
kubectl create token all-ns-user --duration 5h
```

**Duration Format:**
The duration format is based on Go time duration syntax. You can use:

- h for hours (e.g., 5h for 5 hours),
- m for minutes (e.g., 30m for 30 minutes),
- s for seconds (e.g., 120s for 120 seconds)

---
