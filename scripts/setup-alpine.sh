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
        check_result "$step_name (cn)" $? 1
    else
        sed -i "s|dl-cdn.alpinelinux.org|${APK_REPO_GLOBAL}|g" /etc/apk/repositories
        check_result "$step_name (global)" $? 1
    fi
    check_result "$step_name" "1"
}

set_pip_repo(){
    local step_name="set pip repo"
    info_step "$step_name"
    if [ "$NETWORK" = "cn" ]; then
        # pip config set global.index-url ${PIP_REPO_CN}
        domain=$(echo $PIP_REPO_CN | awk -F/ '{print $3}')
        # pip config set global.trusted-host $domain
        # echo "pip config set global.index-url ${PIP_REPO_CN}"
        # echo "pip config set global.trusted-host $domain"
        mkdir -p /etc/pip
        cat > /etc/pip.conf <<EOF
[global]
index-url = $PIP_REPO_CN
trusted-host = $domain
EOF
        check_result "$step_name (cn)" $? 1
    fi
    check_result "$step_name" $? 1
}


dup_env_path(){
    local step_name="dup env path"
    info_step "$step_name"
    PATH=$(echo "$PATH" | tr ':' '\n' | sort -u | tr '\n' ':' | sed 's/:$//')
    echo "$PATH"

    export PATH=$PATH
    # sed -i "s|^export PATH= *||g" /etc/profile
    echo "export PATH=\$(echo \"\$PATH\" | tr ':' '\n' | sort -u | tr '\n' ':' | sed 's/:$//')" >> /etc/profile
    # . /etc/profile
    echo "echo \$PATH"
    info_status "$step_name" "0"
}

default_api() {
    local api="$1"
    # lower api
    api=$(echo "$api" | tr '[:upper:]' '[:lower:]')
    case "$api" in
        set_apk_repo) set_apk_repo;;
        set_pip_repo) set_pip_repo;;
        dup_env_path) dup_env_path;;
        all) set_apk_repo;set_pip_repo;dup_env_path;;
        *) echo "usage: $0 [set_apk_repo|set_pip_repo|dup_env_path]";;
    esac
}

default_api "$@"
