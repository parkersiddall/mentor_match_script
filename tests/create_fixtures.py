"""
Script to create two CSV files populated with mentors and mentees
to be used for testing. 
"""
import random

NUM_MENTORS = 15
NUM_MENTEES = 45
QUESTIONS = [
    {
        'text': 'Favorite color?', 
        'options': ['Red', 'Blue', 'Green', 'Indigo']
    },
    {
        'text': 'Favorite sport?', 
        'options': ['Basketball', 'Soccer', 'Rugby']
    },
    {
        'text': 'Favorite movie?', 
        'options': ['Armagedon', 'Toy Story', 'Forrest Gump', 'Inception']
    },
    {
        'text': 'Favorite TV show?', 
        'options': ['Friends', 'Seinfeld', 'Entourage', 'Scrubs']
    },
    {
        'text': 'Favorite food?', 
        'options': ['Pizza', 'Sushi', 'Steak', 'Salad']
    },
    {
        'text': 'Favorite color?', 
        'options': ['Red', 'Blue', 'Green', 'Indigo']
    },
]

def main():
    mentors: list[object] = []
    mentees: list[object] = []

    for i in range(NUM_MENTORS):
        mentor = create_fake_student(i)
        mentors.append(mentor)

    pass


def create_fake_student(i: int) -> object:
    """
    Creates a student with randomly generated responses. 
    """
    student = {}
    student['NAME'] = f"Name {i}"
    student['SURNAME'] = f"Surname {i}"
    student['EMAIL'] = f"student.{i}@test.com"

    for question in QUESTIONS:
        question_text = question['text']
        random_anwser = 1 # TODO
        student[question_text] = random_anwser

    return student


if __name__ == "__main__":
    main()
