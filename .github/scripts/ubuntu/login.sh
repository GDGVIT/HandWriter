#!/usr/bin/expect -f

set timeout -1
spawn fbs login
expect "Username:"
send -- "SaurusXI\r"
expect "Password:"
send -- "YeahScienceBitch\r"