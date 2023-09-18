# Greener Homes Dashboard
This repo contains all the necessary files for generating your own copy of the GH Tableau Dashboard. You will need to download and locally house all data included in the dashboard. 

If you have any questions, please reach out to brandon.elford@nrcan-rncan.gc.ca for assistance. 

## Requirements
Below is a list of necessary applications and software to generate or update the dashboard:
* Python 3
   * including Pip
* Tableau Prep
* Tableau Desktop

## Required Data
Below is a list of data currently used in the dashboard:
* Application data
  * [Greener Homes Application History](https://nrcan-gc-ca.lightning.force.com/lightning/r/Report/00O2B000000X0K2UAK/view?queryScope=userFolders)
     * Edit the date range and download all history to ```Data Prep/GH Alt Dataset/.``` using the format ```GH History Dates YYYY-MM-DD YYYY-MM-DD.csv``` using the date range chosen in Salesforce.
  * [Greener Homes Completed Applications](https://nrcan-gc-ca.lightning.force.com/lightning/r/Report/00O2B000000X0JsUAK/view?queryScope=userFolders)
     * Download to ```Data Prep/GH Retrofit Dataset/.``` using the format ```GH All Retrofits YYYY-MM-DD.csv``` using todays date
* Map files.
  * [Population Aggregates by FSA](https://041gc.sharepoint.com/:f:/s/EETSPIE-SEETEIPE/EsNiTo2rH09IvKpCfk8-7UYBgufLZR6mJeI0C7H34PdImA?e=eNRlJg)
     * Place in ```Files for Tableau/Shapes Files/.```, though you may need to request for access from the repository admin.

## Common Issues
### Collecting all necessary data
When downloding this repository you will be required to collect all of the Greener Homes Salesforce history to fully populate the dashboard. This step is only required when first downloading this dashboard repository. You are recommended to download the ``Application data" by year, (i.e. change the filters on Salesforce to show data up until 01/01/22, then between 01/01/22-01/01/23, etc) because the entire history in a single file is very large. 
