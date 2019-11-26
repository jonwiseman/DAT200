This repository contains files related to the final project for DAT200: Data Analytics 1

## Goal  
This project aims to create a simple database for storing relevant data for a hypothetical fantasy football webservice.

## Methodology  
Football statistics were collected from a publicly available Kaggle [dataset](https://www.kaggle.com/zynicide/nfl-football-player-stats) and a database schema was designed by group members.  All work was done in a MySQL database created using MySQL Workbench.  The Jupyter notebooks contained in the Notebooks folder detail the steps needed to format the dataset; running the script in the Scripts folder will accomplish the same task.  Note that running the notebooks or scripts is not deterministic, and a different set of users and names will be generated each time.  There is also some formatting of the resulting CSV files that needs to be done in order to import data to MySQL workbench.  

The Entity-Relationship Diagram below shows the outline of our database:

![ERD](https://github.com/jonwiseman/DAT200/raw/master/Images/ERD.png)

## Files  
Below is an overview of what is contained in each folder.

**Data**  
The Data folder contains all relevant data, including CSV files, Pickles used in creation of the tables, and SQL scripts and MySQL workbench files.  CSV contains all CSV files output by the notebooks and scripts.  Pickles exists to store the intermediate steps in table creation and to save progress.  SQL contains a SQL script to create the fantasyFootball database (create_database.sql) and the MySQL workbench file that contains the ERD and can be used to generate the script (fantasyFootball.mwb).

**Docs**  
The Docs folder contains all relevant documents for the project, including a thorough description of the project motivation and rules and all sample queries.  Requirements.txt contains the list of required modules for running generate_files.py.

**Images**  
The Images folder contains an image of the ERD as well as portions of the results of several sample queries.

**Notebooks**  
The Notebooks folder contains two Jupyter notebooks that detail the data cleaning and preparation phases.

**Scripts**  
The Scripts folder contains a Python script that can generate CSV files for uploading into a MySQL workbench file.
