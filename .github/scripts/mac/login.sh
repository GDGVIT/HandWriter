#!/usr/bin/expect -f

set timeout -1
spawn fbs login
expect "Username:"
send_user "$env(FBS_USER)\r"
expect "Password:"
send_user "$env(FBS_PASS)\r"