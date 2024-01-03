@echo off
rem This batch file assumes that you have installed the glabtop2 environment using: conda env create -f environment.yml
call conda activate glabtop2
streamlit run main.py
call conda deactivate
pause