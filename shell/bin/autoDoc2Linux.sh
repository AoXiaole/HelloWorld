#!/bin/bash
if [ $# -eq 1 ];then
    p=$1
else
    p=${PWD}
fi

if [ -f ${p} ];then
	file_type=$(file --mime-type $p | sed "s/^.*: \(.*\)\/.*$/\1/")
    if [ "${file_type}X" == "textX" ];then
		sed -i 's/\r//g' ${p}
		echo "$p success"
	fi
elif [ -d ${p} ];then
    for i in `find ${p} -type f`
    do
	    file_type=$(file --mime-type $i | sed "s/^.*: \(.*\)\/.*$/\1/")
        if [ "${file_type}X" == "textX" ];then
            sed -i 's/\r//g' $i    
            echo "$i success"
        fi
    done

else
    echo "${p} is not exist" >&2
    exit 1
fi
exit 0
