#!/bin/sh
set -e

info_status(){
    local msg_body=$1
    local status=$2
    local msg_success="✅"
    local msg_failed="❌"
    local msg_warn="ℹ️"

    if [ $status -eq 0 ]; then
        echo "$msg_success $msg_body"
    elif [ $status -eq 1 ]; then
        echo "$msg_failed $msg_body"
    else
        echo "$msg_warn $msg_body"
    fi
}

check_result(){
    local status=$?
    local msg_body=$1
    local flag_exit=$2

    if [ $status -eq 0 ]; then
        info_status "$msg_body" 0
    else
        info_status "$msg_body" 1
        [ $flag_exit -eq 0 ] && exit 1;
    fi
}

msg_padd(){
    local msg=$1
    local msg_max_len=$2
    local msg_len=${#msg}
    local msg_fill_length=$((($msg_max_len-$msg_len+2)/2))
    local msg_padding=$(printf "%-${msg_fill_length}s" | tr ' ' '-')
    echo "$msg_padding-$msg-$msg_padding" | cut -c 1-$msg_max_len
}
info_step(){
    local msg=$1
    # echo "-------------------------$msg-------------------------"
    msg_padd "$msg" 60
}

set_apk_repo(){
    local step_name="set apk repo"
    info_step "$step_name"
    if [ "$NETWORK" = "cn" ]; then
        sed -i "s|dl-cdn.alpinelinux.org|${APK_REPO_CN}|g" /etc/apk/repositories
    else
        sed -i "s|dl-cdn.alpinelinux.org|${APK_REPO_GLOBAL}|g" /etc/apk/repositories
    fi
    info_status "$step_name" "0"
}
set_apk_repo
