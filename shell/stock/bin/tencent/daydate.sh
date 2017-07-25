#!/bin/bash
if [ $# -ne 1 ];then
	echo "$0 param error"
	exit 1
fi

toppath=$(cd $(dirname $0);pwd)
source ${toppath}/common.ini

g_day=""


function getdaydata()
{
	local k=0
	local url
	local url_value
	url=$(echo "${g_url_data_day_times}" | sed "s/\[stockcode\]/${stockcode}/")

	url_value=$(url_request "${url}")
	if [ $? -ne 0 ];then
		echo "${url} error"
		return 255
	fi
	url_value=${url_value##*=}
	g_day=$(echo ${url_value} | sed 's/\[\([0-9]*\),.*/\1/')
	if [ $? -ne 0 ];then
		return 255
	fi
	local totals=$(echo "${url_value}" | awk -F "|" '{print NF}')
	
	local tmp_url=$(echo "${g_url_data_day_detail}" | sed "s/\[stockcode\]/${stockcode}/")	
	for ((i=0;i<totals;i++))
	do
		url=$(echo "${tmp_url}" | sed "s/\[times\]/$i/")
		url_value=$(url_request "${url}")
		if [ $? -ne 0 ];then
			echo "${url} error"
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

ret=0
stockcode=$1
# 7项
declare -A data_list=()

getdaydata
if [ $? -ne 0 ];then
	exit 1
fi

time_ymd=${g_day}
table_name="day_${stockcode}_${time_ymd}"
create_table_cmd="use ${g_mysql_db};create table ${table_name}(no INT primary key,time_hms TIME,price FLOAT,ffs FLOAT,vol INT,money BIGINT,b_s enum('B','S','M'));"


table_arrt="(no INT,time_hms TIME,price FLOAT,ffs FLOAT,vol INT,money BIGINT,b_s enum('B','S','M'))"

value=$(check_dataTable ${g_mysql_db} ${table_name})
ret=$?
case ${ret} in
	"0")
	ret=0
	;;
	"1")
	ret=1
	;;
	"2")
	value=$(create_db_table ${g_mysql_db} ${table_name} "${table_arrt}" 1)
	ret=$?
	;;
	"3")
	value=$(create_db_table ${g_mysql_db} ${table_name} "${table_arrt}" 0)
	ret=$?
	;;
	"*")
	ret=255
	;;
esac 
if [ ${ret} -ne 0 ];then
	echo "${value}"
	exit 1
fi

#组包插入数据库
for((j=0;j<${#data_list[*]};j++))
do
	temp_list=(${data_list[$j]//// })
	if [ ${#temp_list[*]} -ne 7 ];then
		echo "${data_list[$j]} error"
		continue
	fi  
	insert_cmd="${insert_cmd} (${temp_list[0]},'${temp_list[1]}',${temp_list[2]},${temp_list[3]},${temp_list[4]},${temp_list[5]},'${temp_list[6]}'),"
	
	if ((j%50==0)) || ((j+1==${#data_list[*]}));then
		if [ $j -ne 0 ];then
			insert_cmd="${insert_cmd%,*};"
			db_value=$(db_insert ${g_mysql_db} ${table_name} "${table_column}" "${insert_cmd}")
			if [ $? -ne 0 ];then
				echo "${insert_cmd}"
				echo "${db_value}"
				break
			fi
		insert_cmd=""	
		fi
	fi	
done



