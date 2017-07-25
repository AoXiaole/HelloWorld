#!/bin/bash

toppath=$(cd $(dirname $0);pwd)
source ${toppath}/common.ini

stock_list=$(${toppath}/stocklist.sh)
if [ $? -ne 0 ];then
	log ERROR "monitor getlist error" ${toppath}/logs/stock
	exit 1
fi

tempfifo=$$_fifo

trap "exec 1000>&-;exec 1000<&-;exit 0" 2
mkfifo $tempfifo
exec 1000<>$tempfifo
rm -rf $tempfifo

for ((i=1; i<=30; i++))
do
    echo >&1000
done


for i in ${stock_list}
do
   read -u1000
   {
	${toppath}/daydate.sh $i
	echo "$i $?"
    echo >&1000
   } &

done

wait
echo "done!!!!!!!!!!"



