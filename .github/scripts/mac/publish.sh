#!/usr/bin/bash

set timeout -1
spawn fbs login
expect "Username:"
send -- "SaurusXI\r"
expect "Password:"
send -- "YeahScienceBitch\r"

set timeout -1
spawn fbs release
send_user -- "$env(VERSION)"