#!/usr/bin/expect -f

set timeout -1
spawn fbs runvm ubuntu
expect "*ubuntu:HandWriter*"
send -- "pip install -r requirements.txt && pip install boto3\r"
expect "*ubuntu:HandWriter*"
send -- "fbs release\r"
expect "Release version*"
send -- "$env(VERSION)\r"
expect "*ubuntu:HandWriter*"
send -- "exit\r"
expect eof