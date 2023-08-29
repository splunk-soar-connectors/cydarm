#!/usr/bin/env bash
set -xe
# Script to package soar app

# Create temp dir
tmp_dir=$(mktemp -d)
echo "$tmp_dir"

# Copy required files across
#pyclean ./app
#cp -r ./app "$tmp_dir"
mkdir "$tmp_dir/app"
cp *.svg *.json *.txt *.html *.py "$tmp_dir/app"
# List tmp dir
ls -lR "$tmp_dir"

# Create tar archive
base=$(basename $PWD)
output_file="$base-$(date +'%s').tgz"
tar -zcvf "$output_file" -C "$tmp_dir" app

# List the archive for debugging
tar -tvf "$output_file"
