# fault-tolerance-hw4

## How to Run?

```bash
python3 -m server1
```

```bash
python3 -m server2
```

```bash
python3 -m eVoter
```

## Archetcthture

### Server
Server1 and Server2 has same function, when it recieve request it will pass result to another one.

When Server started, it will try recover from another server
