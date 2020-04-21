#!/usr/bin/expect -f

set timeout -1
spawn fbs runvm fedora
expect "*fedora:HandWriter*"
send -- "pip install -r requirements.txt && pip install boto3\r"
expect "*fedora:HandWriter*"
send -- "fbs release\r"
expect "Release version*"
send -- "$env(VERSION)\r"
expect "*fedora:HandWriter*"
send -- "exit\r"
expect eof