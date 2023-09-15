@ECHO OFF
set home_dir=%cd%
python "%home_dir%\Data Prep\gh_data_clean.py" & echo "Process Complete!" & pause