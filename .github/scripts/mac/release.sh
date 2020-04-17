#!/usr/bin/expect -f

set timeout -1
spawn fbs release
expect "Release version*"
send -- "$env(VERSION)"