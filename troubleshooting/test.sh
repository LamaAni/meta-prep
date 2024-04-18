#!/bin/bash

TARGET="/tmp/speedtest.dump"
TARGET_DATA="${TARGET}.data.dump"

rm -rf $TARGET $TARGET_DATA
curl -Lo "$TARGET" https://github.com/szalony9szymek/large/releases/download/free/large &
cpid="$!"

sleep 5
kill -STOP $cpid
cp $TARGET "$TARGET_DATA"
ln -sf $TARGET_DATA $TARGET
kill -CONT $cpid

wait $cpid
kill $cpid