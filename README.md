# BUDDY MATCH

The Buddy Match program was created to pair incoming college freshmen with upperclassmen based on shared similarities.

## Features

Matching based on:
    -Nationality
    -Program/major

Even distribution of freshmen to upperclassmen based on program/major.
    -For each program/major, BuddyMatch will calculate the ideal freshmen-to-upperclassmen ratio.
    -Regardless of program/major, no upperclassmen will be assigned more than 5 freshmen.

## Usage

1. Prepare CSV files with student data.
    -Two CSV files are needed; one containing student data for the freshman (applicants) and one for the upperclassmen (buddies).
    -Each CSV file must contain 5 columns, the first row should contain the column titles which ***must*** be written as:
        -Name
        -Email
        -Nationality
        -Interests
        -Program
    -Data must be validated (e.g. U.S.A. and USA would be recognized as different nationalities.)
2. Run the program.
    -Buddy Match takes two command line arguments
        1. The first is the CSV file of the **upperclassmen** (buddies).
        2. The second is the CSV file of the **freshmen** (applicants).
        -*If the command line arguments are not CSV files you will receive an error message.*
        -Example:
        ```bash
        $ python buddymatch.py upperclassmendata.csv freshmendata.csv
        ```

    -Provide export file names.
        -After running the program you will be prompted to insert two file names for the export files.
        ***File names must contain .csv at the end***

    -The program should then provide the following message:
    ```bash
    Program executed successfully.
    There are X applicants that were not matched.
    ```
4. Review export files.
    -The program will spit out two export files to the present working directory.
        -One file will provide the matching data with an upperclassmen on each row. You will be able to see all of the freshmen they were assigned.
        -The other file will provide the matching data with a freshman on each row.
