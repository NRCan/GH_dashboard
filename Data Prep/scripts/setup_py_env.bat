@ECHO OFF
set home_dir=%cd%

if exist  "%home_dir%\Data Prep\gh_env\" ( 
 echo "Starting environment..." &  "%home_dir%\Data Prep\gh_env\Scripts\activate.bat" & pause
) else (
 echo "Creating environment..." & python -m venv  "%home_dir%\Data Prep\gh_env" & call  "%home_dir%\Data Prep\gh_env\Scripts\activate.bat" & pip install -r  "%home_dir%\Data Prep\requirements.txt" & echo "Environment ready, executing data cleaning\n" & pause
)