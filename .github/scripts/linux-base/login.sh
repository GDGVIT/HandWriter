#!/usr/bin/expect -f

set timeout -1
spawn fbs gengpgkey
expect "Email address*"
send -- "$env(EMAIL)\r"
expect "Real name*"
send -- "$env(NAME)\r"
expect "Key password*"
send -- "$env(GPG_PASS)\r"
expect eof

spawn fbs login
expect "Username:"
send -- "$env(FBS_USER)\r"
expect "Password:"
send -- "$env(FBS_PASS)\r"
expect eof