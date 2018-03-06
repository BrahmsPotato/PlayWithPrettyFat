
```sequence
participant User
participant ECAP
participant Kettle

User->>Kettle: create/ edit mapping rule file
Kettle->>User: Save Rule file
User->>ECAP: Login
ECAP->>User: show home screen

```

