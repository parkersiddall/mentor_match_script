from sys import argv, exit
import csv
import math

def main():
    # check to be sure the correct number of files are in the command line
    if len(argv) != 3:
        print("Incorrect insertion of files.")
        exit(1)

    # check to be sure they are csv files and the names are correct
    elif ".csv" not in argv[1] or ".csv" not in argv[2]:
        print("Please import csv files only.")
        exit(1)

    # create global variables for saving buddies and applicants
    buddies_dict = []
    applicants_dict = []

    # open buddies file
    with open(argv[1], "r", encoding='utf-8-sig') as buddiescsvfile: #utf-8-sig allows unique characters and is for CSV UTF files
        buddies = csv.DictReader(buddiescsvfile)

        # loop through buddies
        for buddy in buddies:

            # add to dict counter set to 0 to keep track of assignments
            buddy["Assignments"] = 0

            # add keys for eventual assignments
            buddy["Assignment_1"] = None
            buddy["Assignment_2"] = None
            buddy["Assignment_3"] = None
            buddy["Assignment_4"] = None
            buddy["Assignment_5"] = None

            # write info to the buddies dict
            buddies_dict.append(buddy)


    # open applicants csv file
    with open(argv[2], "r", encoding='utf-8-sig') as applicantscsvfile: #utf-8-sig allows unique characters and is for CSV UTF files
        applicants = csv.DictReader(applicantscsvfile)

        # loop through applicants
        for applicant in applicants:

            # set each applicants match status to False
            applicant["Match_Status"] = False

            # add a key in order to track the buddy they are assigned too
            applicant["Buddy"] = None

            # write info to applicants dict
            applicants_dict.append(applicant)

    # MATCHING PHASE 1: CHECK TO SEE IF PROGRAM, NATIONALITY AND INTERESTS ALL MATCH

    # loop through buddies
    for buddy in buddies_dict:

        # loop to go through applicants
        for applicant in applicants_dict:

            # check if the student has already been matched
            if applicant["Match_Status"] == True:
                continue

            # check that buddy is not filled with assignments
            elif buddy["Assignments"] == ideal_number_pairs_(buddies_dict, applicants_dict, buddy["Program"]) \
                    or buddy["Assignments"] == 5:
                break

            # check to see if programs match
            elif buddy["Program"] == applicant["Program"] and buddy["Nationality"] == applicant["Nationality"] \
                    and buddy["Interests"] in applicant["Interests"]:

                make_match(buddy, applicant)

                continue

            else:
                continue

    # MATCHING PHASE 2: CHECK TO SEE IF PROGRAM AND NATIONALITY ARE SAME AND ASSIGN THE MATCH

    # loop through buddies
    for buddy in buddies_dict:

        # loop to go through applicants
        for applicant in applicants_dict:

            # check if the student has already been matched
            if applicant["Match_Status"] == True:
                continue

            # check that buddy is not filled with assignments
            elif buddy["Assignments"] == ideal_number_pairs_(buddies_dict, applicants_dict, buddy["Program"]) \
                    or buddy["Assignments"] == 5:
                break

            # check to see if programs match
            elif buddy["Program"] == applicant["Program"] and buddy["Nationality"] == applicant["Nationality"]:

                make_match(buddy, applicant)

                continue

            else:
                continue


    # MATCHING PHASE 3: MAKE ASSIGNMENTS BASED ONLY ON COURSE PROGRAM

    # loop through buddies
    for buddy in buddies_dict:

        # loop to go through applicants
        for applicant in applicants_dict:

            # check if the student has already been matched
            if applicant["Match_Status"] == True:
                continue

            # check that buddy is not filled with assignments
            elif buddy["Assignments"] == ideal_number_pairs_(buddies_dict, applicants_dict, buddy["Program"]) \
                    or buddy["Assignments"] == 5:
                break

            # check to see if programs match
            elif buddy["Program"] == applicant["Program"]:

                make_match(buddy, applicant)

                continue

            else:
                continue

    # MATCHING PHASE 4: IDENTIFY THE STUDENTS THAT WERE NOT MATCHED AND REQUIRE FURTHER ASSISTANCE

    # create a counter to keep track of how many applicants have not been matched
    no_match_counter = 0

    # run a loop to check each applicants status
    for applicant in applicants_dict:
        if applicant["Match_Status"] == False:
            no_match_counter += 1


    # EXPORT CSV FILES

    # prompt user for filenames
    while True:
        buddies_export_file = input("How do you wish to call the buddies export file? (Must be .csv file): ")
        if ".csv" in buddies_export_file:
            break

    while True:
        applicants_export_file = input("How do you wish to call the applicants export file? (Must be .csv file): ")
        if ".csv" in applicants_export_file:
            break


    # create and save buddies dict to csv file
    with open(buddies_export_file, "w", newline="") as file:
        fieldnames = ["Name", "Program", "Nationality", "Interests", "Email", "Assignments", "Assignment_1", \
                      "Assignment_2", "Assignment_3", "Assignment_4", "Assignment_5"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for buddy in buddies_dict:
            writer.writerow(buddy)

    # create and save applicants to a csv file
    with open(applicants_export_file, "w", newline="") as file:
        fieldnames = ["Name", "Program", "Nationality", "Interests", "Email", "Match_Status", "Buddy"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for applicant in applicants_dict:
            writer.writerow(applicant)


    # print if match completed correctly
    print("Program executed successfully.")
    print("There are", no_match_counter, "applicants that were not matched.")
    exit(0)


# this function returns the key for the next available assignment
def find_assignment_number(buddy):
    if buddy["Assignment_1"] is None:
        return "Assignment_1"
    elif buddy["Assignment_2"] is None:
        return "Assignment_2"
    elif buddy["Assignment_3"] is None:
        return "Assignment_3"
    elif buddy["Assignment_4"] is None:
        return "Assignment_4"
    else:
        return "Assignment_5"

# this function determines the ideal number of applicants to be paired to each student from a given program
def ideal_number_pairs_(buddies, applicants, program):
    applicant_counter = 0
    buddy_counter = 0

    for applicant in applicants:
        if applicant["Program"] == program:
            applicant_counter += 1

    for buddy in buddies:
        if buddy["Program"] == program:
            buddy_counter += 1

    return math.ceil(applicant_counter/buddy_counter)

# this function logs a match by writing the information in the dicts
def make_match(buddy, applicant):
    buddy[find_assignment_number(buddy)] = applicant["Name"] + ";" + applicant["Program"] + ";" \
                                           + applicant["Nationality"] + ";" + applicant["Email"]

    # update buddy assignment count
    buddy["Assignments"] += 1

    # update applicants status and match key
    applicant["Match_Status"] = True
    applicant["Buddy"] = buddy["Name"] + ";" + buddy["Nationality"] + ";" + buddy["Email"]


if __name__ == "__main__":
    main()