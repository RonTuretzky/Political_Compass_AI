#!/usr/bin/bash
git clone https://github.com/RonTuretzky/Political_Compass_AI.git
cd Political_Compass_AI
jupytext --to py main.ipynb --opt comment_magics=false
mv main.py main.ipy
ipython main.ipy >> Results.txt
