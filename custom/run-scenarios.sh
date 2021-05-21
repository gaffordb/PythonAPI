#!/bin/bash

for f in ./scenarios/**/*.py
do
    echo "Running $f..."
    $f
done
