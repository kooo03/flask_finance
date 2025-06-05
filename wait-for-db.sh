#!/bin/sh

host="$1"
port="$2"
shift 2

echo "Waiting for MySQL at $host:$port..."

# 等待 MySQL 容器启动
while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "MySQL is up!"

# 如果有 "--"，再 shift 掉它
if [ "$1" = "--" ]; then
  shift
fi

# 执行真正的命令
exec "$@"
