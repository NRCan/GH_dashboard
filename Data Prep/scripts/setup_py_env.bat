@ECHO OFF
if exist "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\gh_env\" ( 
 echo "Starting environment..." & "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\gh_env\Scripts\activate.bat" & pause
) else (
 echo "Creating environment..." & python -m venv "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\gh_env" & call "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\gh_env\Scripts\activate.bat" & pip install -r "C:\Users\belford\Documents\Projects\Greener Homes\GH Dashboard\Data Prep\requirements.txt" & echo "Environment ready, executing data cleaning\n" & pause
)