#!/bin/bash

PYTHONPATH=./:./rules python -m unittest discover -s rules -p "*.py"
