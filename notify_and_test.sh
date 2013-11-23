#!/bin/bash
#
# test loop for changes, 
#
trap finish INT

function finish() {
  trap "exit 0" INT
  sleep 2
  python -m unittest2  discover -t main main
  exit $?
}

cat << EOF
type ctrl-C to stop with full test
type ctrl-C twice to stop without testing
EOF
while DIR=$(inotifywait -r --format %w -e close_write,delete .) 
do 
  python -m unittest2  discover -t main $DIR 
done
