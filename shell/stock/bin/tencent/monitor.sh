#!/bin/bash

toppath=$(cd $(dirname $0);pwd)
source ${toppath}/common.ini

log INFO "monitor begin" ${g_logfile_stock}

table_name=${g_dbtable_stocklist}
stock_list=$(dbstock_cmd "select stockcode from ${table_name};")
ret=$?
if [ $? -ne 0 ];then
	log ERROR "ret = ${ret} monitor getlist error" ${g_logfile_stock}
	exit 1
fi
stock_list=${stock_list//stockcode/}
tempfifo=$$_fifo

trap "exec 1000>&-;exec 1000<&-;exit 0" 2
mkfifo $tempfifo
exec 1000<>$tempfifo
rm -rf $tempfifo

for ((i=1; i<=50; i++))
do
    echo >&1000
done


for i in ${stock_list}
do
   read -u1000
   {
	${toppath}/daydate.sh $i
	log DEBUG "$i $?" ${g_logfile_stock}
    echo >&1000
   } &

done

wait
log DEBUG "$0 done!!!!!!!!!! [`date +%Y%m%d`]" ${g_logfile_stock}




