#!/bin/bash

toppath=$(cd $(dirname $0);pwd)
source ${toppath}/common.ini

url_value=$(url_request "${g_url_stockList}")
if [ $? -ne 0 ];then
	log ERROR "get stock list error" ${g_logfile_stock}
	exit 1
fi
url_value=${url_value##*=}
temp=$(echo ${url_value} | sed "s/.*data:'\(.*\)'.*/\1/")

insert_values=""
url_value="${temp//,/ } "

table_name=${g_dbtable_stocklist}
table_arrt="(stockcode char(10) primary key)"
value=$(dbstock_create_table ${table_name} "${table_arrt}")
ret=$?
if [ ${ret} -ne 0 ];then
	log ERROR "ret = ${ret} ${value} $LINENO" ${g_logfile_stock}
	exit 1
fi
sql_stocklist=$(dbstock_cmd "select stockcode from ${table_name};")

for i in ${sql_stocklist}
do
	url_value=${url_value//$i / }
done

data_list=(${url_value})

num=${#data_list[*]}
for((j=0;j<${num};j++))
do
	insert_values="${insert_values} ('${data_list[j]}'),"
	if (((j+1)%50==0)) || ((j+1==${num}));then
		
		insert_values="${insert_values%,*};"
		db_value=$(dbstock_insert ${table_name} "${insert_values}")
		ret=$?
		if [ ${ret} -ne 0 ];then
			log ERROR "ret=${ret},${insert_values} value=${db_value} $LINENO" ${g_logfile_stock}
			break
		fi
		insert_values=""	

	fi	
done
log DEBUG "run" ${toppath}/logs/stockadd
if [ ${num} -ne 0 ];then
	log DEBUG "${data_list[*]}" ${toppath}/logs/stockadd
fi

exit 0
