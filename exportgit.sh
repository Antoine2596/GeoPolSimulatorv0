#!/bin/bash

time=$(date +%Y-%m-%d-%H-%M)
git add .
git commit -m "update $time"
git push origin main

echo
echo "push update $time"
echo