#! /bin/sh

if [ "$#"  -lt 3 ];
then
    echo "参数个数小于3"
    exit
fi

ssh_tag=$1
session_id=$2
logpath=$3
#循环获取到获取远程主机ssh的pid，原因监控先于ssh登陆
for i in `seq 1 30`
do
    #获取远程主机ssh的pid
    process_id=`ps aux|grep $ssh_tag|grep -v grep|grep -v sshpass|grep -v $0|awk '{print $2}'`

    #如果不为空，即获取到了pid
    if [ !  -z $process_id ] ;
    then
        sudo strace  -fp $process_id -t -o  "$logpath/session_"$session_id"_"$ssh_tag".log"
        break
    else
	    sleep 1
    fi

done
