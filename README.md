# Greener Homes Dashboard
This repo contains all the necessary files for generating your own copy of the GH Tableau Dashboard. You will need to download and locally house all data included in the dashboard. Below is a list of data currently used in the dashboard:
* Application data
  * [Greener Homes Application History](https://nrcan-gc-ca.lightning.force.com/lightning/r/Report/00O2B000000X0K2UAK/view?queryScope=userFolders)
     * Edit the date range and download all history to ```Data Prep/GH Alt Dataset/.``` using the format ```GH History Dates YYYY-MM-DD YYYY-MM-DD.csv``` using the date range chosen in Salesforce.
  * [Greener Homes Completed Applications](https://nrcan-gc-ca.lightning.force.com/lightning/r/Report/00O2B000000X0JsUAK/view?queryScope=userFolders)
     * Download to ```Data Prep/GH Retrofit Dataset/.``` using the format ```GH All Retrofits YYYY-MM-DD.csv``` using todays date
* Map files.
  * [Population Aggregates by FSA](https://041gc.sharepoint.com/:f:/s/EETSPIE-SEETEIPE/EsNiTo2rH09IvKpCfk8-7UYBgufLZR6mJeI0C7H34PdImA?e=eNRlJg)
     * Place in ```Files for Tableau/Shapes Files/.```, though you may need to request for access from the repository admin.

If you have any questions, please reach out to brandon.elford@nrcan-rncan.gc.ca for assistance. 
