#!/bin/bash

toppath=$(cd $(dirname $0);pwd)
source ${toppath}/common.ini

ret=0

g_day=""
today_ymd=`date +%Y%m%d`
stockcode=sh000001
function getdaydata()
{
	local k=0
	local url
	local url_value
	url=$(echo "${g_url_data_day_times}" | sed "s/\[stockcode\]/${stockcode}/")

	url_value=$(url_request "${url}")
	if [ $? -ne 0 ];then
		log ERROR "${url} error $LINENO" ${g_logfile_stock}
		return 255
	fi
	##add by aoml 测试日志
	log WARNING "${url_value}" ${toppath}/logs/stockcalendar
	
	url_value=${url_value##*=}
	g_day=$(echo ${url_value} | sed 's/\[\([0-9]*\),.*/\1/')
	if  [ ! "${g_day}"x = "${today_ymd}"x ] ;then
        log WARNING "${stockcode} ${g_day} is not today" ${g_logfile_stock}
		return 255
	fi
	return 0
}


getdaydata
if [ $? -ne 0 ];then
	exit 1
fi

time_ymd=`date +%Y-%m-%d`
table_name=${g_dbtable_stockcalendar}

table_arrt="(day DATE primary key)"

value=$(dbstock_create_table ${table_name} "${table_arrt}")
ret=$?
if [ ${ret} -ne 0 ];then
	log ERROR "${value}" ${g_logfile_stock}
	exit 1
fi

#组包插入数据库
value=$(dbstock_insert ${table_name} "('${time_ymd}')")
if [ $? -ne 0 ];then
    log ERROR "insert time error value=${value}" ${g_logfile_stock}
    exit 1
fi
exit 0


