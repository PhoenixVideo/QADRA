# Building instructions

The software is tested in Windows OS. The steps to build the project in Windows are explained below.

## Prerequisites
 1. [Python](https://www.python.org/) version 3.12 or higher.

## Instructions to run 

  1. Open Command prompt and Clone Repository :
  
     git clone `<repository_url>`

  2. Navigate to Project Directory :

     cd `<project_directory>`
	 
  3. Create and Activate Virtual Environment:

     python -m venv `<venv_name>`
     
     <venv_name>\Scripts\activate

  4. Install Dependencies:

     pip install -r requirements.txt

  6. Run the Application with the required CLI option and corresponding values:

     Sample command line:

     `python main.py --maxEncTime 100 --maxDecTime 200 --codec vvenc --resultCsv output.csv --rmax 1080 --maxQuality 90 --jnd 5`

  7. Deactivate Virtual Environment:
  
     deactivate


Make sure to replace `<repository_url>`, `<project_directory>`, and `<venv_name>` with the appropriate values for the project. Step 1 and Step 4 have to be done only the first time.

