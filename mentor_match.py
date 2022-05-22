import csv
import argparse
from sys import exit
import math


class Student:
    def __init__(self, name, surname, email, is_mentor=False):
        self.name: str = name
        self.surname: str = surname
        self.email: str = email
        self.responses: object = {}
        self.is_mentor: bool = is_mentor
        self.matches: list = []


class Match:
    def __init__(self, mentor, mentee, match_rate):
        self.mentor: Student = mentor
        self.mentee: Student = mentee
        self.match_rate: int = match_rate


def main():
    parser = argparse.ArgumentParser(
        description="Pairs mentees with a best fit mentor.",
    )
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument(
        "--mentors",
        type=str,
        help="Filepath to the csv file with mentors to process.",
        required=True,
    )
    required_args.add_argument(
        "--mentees",
        type=str,
        help="Filepath to the csv file with mentees to process.",
        required=True,
    )
    args = parser.parse_args()

    mentors: list[Student] = process_csv_file(args.mentors, True)
    mentees: list[Student] = process_csv_file(args.mentees)
    matching_ratio: int = find_match_ratio(mentors, mentees)
    matching_params = list(mentors[0].responses.keys())
    matches = []

    if matching_ratio == 0:
        print("ERROR: There aren't enough applicants to make matches.")
        exit(1)

    if not validate_responses(matching_params, mentors, mentees):
        print("ERROR: The questions that were asked to applicants are not consistent.")
        exit(1)

    for i in range(len(matching_params), -1, -1):
        for mentee in mentees:
            if len(mentee.matches) == 1:
                continue
            for mentor in mentors:
                if len(mentor.matches) == matching_ratio:
                    continue

                match_points = 0
                for param in matching_params:
                    if mentee.responses[param] == mentor.responses[param]:
                        match_points += 1

                if match_points == i:
                    match_rate = 0 if i==0 else math.ceil((i/len(matching_params)) * 100)
                    mentor.matches.append(mentee)
                    mentee.matches.append(mentor)
                    match = Match(mentor, mentee, match_rate)
                    matches.append(match)
                    break

    write_matches_to_csv(matches)
    write_unmatched_to_csv(mentors + mentees)


def process_csv_file(filepath: str, is_mentor_file=False) -> list:
    """
    Reads a CSV file and saves it to memory as an array of Students.
    """
    try:
        students = []
        with open(filepath, "r", encoding='utf-8-sig') as f:
            rows = csv.DictReader(f)
            for row in rows:
                student = Student(row["NAME"], row["SURNAME"], row["EMAIL"])
                del row["NAME"], row["SURNAME"], row["EMAIL"]
                student.responses = row
                students.append(student)
                if is_mentor_file:
                    student.is_mentor = True
        return students
    except (FileNotFoundError):
        print(f"ERROR: The file {filepath} does not exist.")
        exit(1)
    except (KeyError):
        print(
            "ERROR: One or both of your csv files is not properly titled."
            "Requried columns are 'NAME', SURNAME', and 'EMAIL'."
        )
        exit(1)


def find_match_ratio(mentors: list, mentees: list) -> int:
    """
    Determines how many mentees should be assigned to each mentor.
    """
    if not len(mentors) or not len(mentees):
        return 0
    else:
        ratio = len(mentees) / len(mentors)
        return math.ceil(ratio)


def validate_responses(match_params: list, mentors: list, mentees: list) -> bool:
    """
    Checks to be sure the same questions were asked to all mentors and mentees
    """
    all_applicants = mentors + mentees
    for applicant in all_applicants:
        if sorted(list(applicant.responses.keys())) != sorted(match_params):
            return False
    return True


def get_unmatched_students(students: list) -> list:
    """
    Returns a list of students that were not matched with a mentor or mentee.
    """
    unmatched = []
    for student in students:
        if len(student.matches) == 0:
            unmatched.append(student)
    return unmatched


def write_matches_to_csv(matches: list) -> None:
    """
    Creates a csv file and writes the data to it.
    """
    fieldnames = [
        'mentor_name',
        'mentor_surname',
        'mentor_email',
        'mentee_name',
        'mentee_surname',
        'mentee_email',
        'match_rate',
        ]
    
    questions = matches[0].mentor.responses.keys()
    for question in questions:
        fieldnames.append(f"mentor_{question}")
        fieldnames.append(f"mentee_{question}")

    with open('matches.csv', "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for match in matches:
            match_dict = {
                'mentor_name': match.mentor.name,
                'mentor_surname': match.mentor.surname,
                'mentor_email': match.mentor.email,
                'mentee_name': match.mentee.name,
                'mentee_surname': match.mentee.surname,
                'mentee_email': match.mentee.email,
                'match_rate': f"{match.match_rate}%",
            }
            for question in questions:
                match_dict[f"mentor_{question}"]= match.mentor.responses[question]
                match_dict[f"mentee_{question}"]= match.mentee.responses[question]

            writer.writerow(match_dict)


def write_unmatched_to_csv(unmatched: list) -> None:
    """
    Creates a csv file with all of the students that didn't get a match.
    """
    fieldnames = [
        'applicant_type',
        'name',
        'surname',
        'email',
    ]

    with open('unmatched.csv', "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for student in unmatched:
            if len(student.matches) == 0:
                student_dict = {
                    'applicant_type': 'mentor' if student.is_mentor else 'mentee',
                    'name': student.name,
                    'surname': student.surname,
                    'email': student.email,
                }
                writer.writerow(student_dict)


if __name__ == "__main__":
    main()
