#! /bin/sh

if [ "$#"  -lt 1 ];
then
    echo "参数个数小于1"
    exit
fi

ssh_tag=$1
echo $ssh_tag
#循环获取到获取远程主机ssh的pid，原因监控先于ssh登陆
for i in `seq 1 30`
do
    #获取远程主机ssh的pid
    process_id=`ps aux|grep $ssh_tag|grep -v grep|grep -v sshpass|grep -v $0|awk '{print $2}'`

    #如果不为空，即获取到了pid
    if [ !  -z $process_id ] ;
    then
        today=`date  "+%Y%m%d"`
        dir="/tmp/$today/"
        mkdir -p dir
        sudo strace  -fp $process_id -t -o  "$dir/session_$ssh_tag.log"
        break
    else
	    sleep 1
    fi

done
