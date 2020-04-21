#!/usr/bin/expect -f

set timeout -1
spawn fbs runvm arch
expect "*arch:HandWriter*"
send -- "pip install -r requirements.txt && pip install boto3\r"
expect "*arch:HandWriter*"
send -- "fbs release\r"
expect "Release version*"
send -- "$env(VERSION)\r"
expect "*arch:HandWriter*"
send -- "exit\r"
expect eof