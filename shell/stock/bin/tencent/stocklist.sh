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
url_value=${temp//,/ }
data_list=(${temp//,/ })
table_name=${g_dbtable_stocklist}

for((j=0;j<${#data_list[*]};j++))
do
	insert_values="${insert_values} ('${data_list[j]}'),"
	
	if ((j%50==0)) || ((j+1==${#data_list[*]}));then
		if [ $j -ne 0 ];then
			insert_values="${insert_values%,*};"
			db_value=$(dbstock_insert ${table_name} "${insert_values}")
			ret=$?
			if [ ${ret} -ne 0 ];then
				log ERROR "ret=${ret},${insert_values} value=${db_value} $LINENO" ${g_logfile_stock}
				break
			fi
		insert_values=""	
		fi
	fi	
done

#echo -e 使得 \n 起作用
##add by aoml for 测试
echo "${url_value}" > ${toppath}/logs/stocklist_`date +%H_%M_%S`

echo "${url_value}"
exit 0
