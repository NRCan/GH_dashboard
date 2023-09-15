@ECHO OFF
set home_dir=%cd%
python "%home_dir%\Data Prep\gen_forecast.py" & echo "Forecasting Complete!" & pause