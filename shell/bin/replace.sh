#!/bin/bash
if [ $# -ge 2 ];then
    oldstr=$1
	newstr=$2
	if [ $# -eq 3 ];then
		p=$3
	else
		p=${PWD}
	fi
else
    echo "usage: replace oldstr newstr [<file|dir>] >&2"
fi

if [ -f ${p} ];then
	file_type=$(file --mime-type $p | sed "s/^.*: \(.*\)\/.*$/\1/")
    if [ "${file_type}X" == "textX" ];then
		sed -i "s/${oldstr}/${newstr}/g" ${p}
		echo "$p success"
	fi
elif [ -d ${p} ];then
    for i in `find ${p} -type f`
    do
	    file_type=$(file --mime-type $i | sed "s/^.*: \(.*\)\/.*$/\1/")
        if [ "${file_type}X" == "textX" ];then
            sed -i "s/${oldstr}/${newstr}/g" $i    
            echo "$i success"
        fi
    done

else
    echo "${p} is not exist" >&2
    exit 1
fi
exit 0
