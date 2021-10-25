#!/bin/bash

git submodule update --init

docker build -t scenario-runner

# To run (with display)
# docker run --rm -it --net=host -e DISPLAY=$DISPLAY scenic-runner <cmd>
