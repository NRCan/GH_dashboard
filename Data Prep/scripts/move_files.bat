@ECHO OFF
set home_dir=%cd%

echo "Moving files to correct directories..."

move /Y "%home_dir%\Data Prep\dim_week_projection.csv" "%home_dir%\Files for Tableau Prep"
move /Y "%home_dir%\Data Prep\dim_week.csv" "%home_dir%\Files for Tableau Prep"
move /Y "%home_dir%\Data Prep\dim_month.csv" "%home_dir%\Files for Tableau Prep"
move /Y "%home_dir%\Data Prep\final_dataset.csv" "%home_dir%\Files for Tableau Prep"

move /Y "%home_dir%\Data Prep\retrofit_running_sum_all_provinces.csv" "%home_dir%\Files for Tableau"
move /Y "%home_dir%\Data Prep\recipients_by_postal_code.csv" "%home_dir%\Files for Tableau"
move /Y "%home_dir%\Data Prep\applicants_by_postal_code.csv" "%home_dir%\Files for Tableau"

echo "Files successfully moved!" & pause