#!/usr/bin/expect -f

set timeout -1
spawn fbs runvm ubuntu
expect "*(venv) ubuntu:HandWriter$ "
send -- "yes | apt-get install expect && export VERSION=1.0.1 && ./.github/scripts/release.sh && exit"