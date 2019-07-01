#!/bin/bash
source ~/.bashrc
shell_path=$(cd `dirname $0`;pwd)
cd $shell_path
option=$1



function _start()
{
    echo "start app"
    uwsgi -d $shell_path/httplog.log --ini $shell_path/uwsgi.ini
}

function _stop()
{
    echo "stop app"
    pid=`cat $shell_path/uwsgi.pid`
    kill -3 $pid
    while test -n "`ps -f --pid $pid  --no-heading`"
    do
        sleep 0.1
    done
}

case "$option" in
    "start" )
        _start
    ;;
    "stop" )
        _stop
    ;;
   "restart" )
        _stop
        _start
    ;;
    *)
        echo "Usage: start.sh [option]"
        echo ""
        echo "  start : start app"
        echo "  stop : stop app"
        echo "  restart : restart app"
    ;;
    
esac

