#!/bin/bash

PYTHONPATH=./:./rules python2 -m unittest discover -s rules -p "*.py"
