@ECHO OFF
echo "Moving files to correct directories..."

move /Y "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\dim_week_projection.csv" "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Files for Tableau Prep"
move /Y "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\dim_week.csv" "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Files for Tableau Prep"
move /Y "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\dim_month.csv" "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Files for Tableau Prep"
move /Y "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\final_dataset.csv" "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Files for Tableau Prep"

move /Y "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\retrofit_running_sum_all_provinces.csv" "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Files for Tableau"
move /Y "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\recipients_by_postal_code.csv" "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Files for Tableau"
move /Y "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\applicants_by_postal_code.csv" "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Files for Tableau"

echo "Files successfully moved!" & pause