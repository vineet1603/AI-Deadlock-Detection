#!/bin/bash
echo "Checking for deadlocks..."
lsof -n | grep DEL
