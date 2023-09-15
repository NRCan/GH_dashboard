@ECHO OFF

echo "Begining GH dashboard data prep..." & pause

call "Data Prep"\scripts\setup_py_env.bat & call "Data Prep"\scripts\data_clean.bat & call "Data Prep"\scripts\move_files.bat & call "Data Prep"\scripts\forecasting.bat

echo "Ready for the Tableau Prep step!"
echo "You may now exit this window." & pause
