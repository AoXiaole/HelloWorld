#!/bin/bash

toppath=$(cd $(dirname $0);pwd)
source ${toppath}/common.ini

url_value=$(url_request "${g_url_stockList}")
if [ $? -ne 0 ];then
	log ERROR "get stock list error" ${toppath}/logs/stock
	exit 1
fi
url_value=${url_value##*=}
temp=$(echo ${url_value} | sed "s/.*data:'\(.*\)'.*/\1/")
echo ${temp//,/ }
exit 0
