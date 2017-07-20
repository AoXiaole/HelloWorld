#!/bin/bash
logLevel=DEBUG

#有些地方使用空格不方便，所以使用了不可见字符代替空格，也避免了冲突
invisible_A="^A"
blank=" "

declare -A level_map=()
level_map["DEBUG"]=1
level_map["INFO"]=2
level_map["WARNING"]=3
level_map["ERROR"]=4
level_map["FATAL"]=5

#通过字符串得带在 transcoder.ini 中对应的值
function getValueFromTranscoder()
{
      	local value=`grep  "^[[:blank:]]*$1=" ${file_transcoder_ini}`
        value=${value##*=}
        value=${value%%#*}
        
        echo ${value}
}

logLevel=$(getValueFromTranscoder "logLevel")
if [ -z "${level_map[${logLevel}]}" ];then
	logLevel=DEBUG
fi
#打印日志，格式为：log LEVEL "msg" outlogFile “不带后缀”
function log()
{
	if [ $# -lt 2 ];then
		echo "log param error"
			return
	fi

	if [ $# -eq 3 ];then
		local outLogFile=$3
	else
		local outLogFile=${log_dir}/monitor/monitor_task		
	fi
	local outLogDir=$(dirname ${outLogFile})
	local level=$1
	local str=$2
	local ls_value
	local file_size
	local time_

	if [ ! -d ${outLogDir} ];then
		mkdir -p ${outLogDir}
	fi
	
	if [ -z "${level_map[${level}]}" ] || [ ${level_map[${level}]} -ge ${level_map[${logLevel}]} ];then
		
		time_=`date +%Y-%m-%d-%H:%M:%S`
		echo "[${time_}] [${level}] ${str}" >> ${outLogFile}.log
		
		ls_value=`ls -l ${outLogFile}.log 2>&1`
		if [ $? -ne 0 ];then
			return
		fi
		
		file_size=`echo "${ls_value}" | head -1 | awk '{print int($5/1024/1024)}'`
	
		if [ ! -z "${file_size}" ] && [ ${file_size} -ge 20 ];then
			local log_name="${outLogFile}.$(date +%Y%m%d%H%M%S)"
			mv ${outLogFile}.log ${log_name}.log
		fi
	fi

}

#获取 当前进程，以及由当前进程产生的进程 的 pid
# $(getMyAndSonsPid "${ps_pid_ppid}" ${my_pid})
# ps_pid_ppid="$(ps -eo pid,ppid)"
function getMyAndSonsPid()
{
    if [ $# -ne 2 ];then
        return 1
    fi
    local   ps_pid_ppid=$1
    local   my_pid=$2
    local   my_sonpid
    local   pids="${my_pid}"
    my_sonpid=`echo "${ps_pid_ppid}" | awk -v apid="${my_pid}" '{if ($2==apid) print $1}'`
    if [ $? -ne 0 ];then
	    echo "${pids}"
		return 1
	fi

	if [ ! -z "${my_sonpid}" ];then
        for i in ${my_sonpid}
        do
            pids="${pids} "$(getMyAndSonsPid "${ps_pid_ppid}" $i)
        done
    fi

    echo "${pids}"
    return 0
}

#获取同名的其他进程的Pid
function getOtherSameNameProcessPid()
{
	if [ $# -ne 2 ];then
		return 1
	fi
	local sh_cmd=$1
	local my_pid=$2	
	local pid_ppid
	local myPids
	local ps_pid
	local p

	pid_ppid=`ps -eo pid,ppid,cmd | grep "${sh_cmd}" | grep -v "grep" | awk '{print $1,$2}'`
	if [ $? -ne 0 ];then
		return 1
	fi

	myPids=$(getMyAndSonsPid "${pid_ppid}" ${my_pid})
	if [ $? -ne 0 ];then
		return 1
	fi
	
	ps_pid=`echo "${pid_ppid}" | awk '{print $1}'`
	ps_pid="`echo ${ps_pid}`${blank}"

    for p in ${myPids}
	do
		ps_pid=${ps_pid//${p}${blank}/${blank}}
	done	
	echo ${ps_pid}
	return 0
}

