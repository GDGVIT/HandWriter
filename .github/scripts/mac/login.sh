#!/usr/bin/expect -f

set timeout -1
spawn fbs login
expect "Username:"
send -- "$env(FBS_USER)"
expect "Password:"
send -- "$env(FBS_PASS)"