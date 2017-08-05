#!/bin/bash
if [ $# -ne 1 ];then
	echo "$0 param error"
	exit 1
fi

toppath=$(cd $(dirname $0);pwd)
source ${toppath}/common.ini

ret=0
stockcode=$1

g_day=""
today_ymd=`date +%Y%m%d`

function getdaydata()
{
	local k=0
	local url
	local url_value
	url=$(echo "${g_url_data_day_times}" | sed "s/\[stockcode\]/${stockcode}/")

	url_value=$(url_request "${url}")
	if [ $? -ne 0 ];then
		log ERROR "${stockcode} ${url} error" ${g_logfile_stock}
		return 255
	fi
	url_value=${url_value##*=}
	g_day=$(echo ${url_value} | sed 's/\[\([0-9]*\),.*/\1/')
	if [ -z "${g_day}" ] ;then
        log ERROR "${stockcode} ${g_day} is not today" ${g_logfile_stock}
		return 255
	fi
	if [ "${g_day}x" != "${today_ymd}x" ] ;then
        #log ERROR "${stockcode} ${g_day} is not today " ${g_logfile_stock}
		#return 255
		:
	fi
	local totals=$(echo "${url_value}" | awk -F "|" '{print NF}')
	
	local tmp_url=$(echo "${g_url_data_day_detail}" | sed "s/\[stockcode\]/${stockcode}/")	
	for ((i=0;i<totals;i++))
	do
		url=$(echo "${tmp_url}" | sed "s/\[times\]/$i/")
		url_value=$(url_request "${url}")
		if [ $? -ne 0 ];then
			log ERROR "${stockcode} ${url} error" ${g_logfile_stock}
		fi
		temp_list=($(echo "${url_value##*=}" | grep -o '".*"' | tr '"|' ' '))
		for ((j=0;j<${#temp_list[*]};j++))
		do
			data_list[${k}]=${temp_list[$j]}
			let k++
		done
	done
	return 0
}

# 7项
declare -A data_list=()

getdaydata
if [ $? -ne 0 ];then
	exit 1
fi

time_ymd=${g_day}

table_name="day_${stockcode}_${time_ymd}"

table_arrt="(no INT primary key,time_hms TIME,price FLOAT,ffs FLOAT,vol INT,money BIGINT,b_s enum('B','S','M'))"

dbstock_cmd "drop table ${table_name};" &>/dev/null

value=$(dbstock_create_table ${table_name} "${table_arrt}")
ret=$?

if [ ${ret} -ne 0 ];then
	log ERROR "${stockcode} ret = ${ret} ${value} $LINENO" ${g_logfile_stock}
	exit 1
fi
num=${#data_list[*]}
#组包插入数据库
for((j=0;j<${num};j++))
do
	temp_list=(${data_list[$j]//// })
	if [ ${#temp_list[*]} -ne 7 ];then
		log ERROR "${stockcode} ${data_list[$j]} error $LINENO" ${g_logfile_stock}
		continue
	fi  
	insert_cmd="${insert_cmd} (${temp_list[0]},'${temp_list[1]}',${temp_list[2]},${temp_list[3]},${temp_list[4]},${temp_list[5]},'${temp_list[6]}'),"
	
	if (((j+1)%20==0)) || ((j+1==${num}));then
		
		insert_cmd="${insert_cmd%,*};"
		db_value=$(dbstock_insert ${table_name} "${insert_cmd}")
		if [ $? -ne 0 ];then
			log ERROR "${stockcode} ${insert_cmd} value=${db_value} $LINENO" ${g_logfile_stock}
			break
		fi
		insert_cmd=""	
	fi
	
done
exit 0


