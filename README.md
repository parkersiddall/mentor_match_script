# MENTOR MATCH
A script that matches mentees with a best fit mentor. The program was written for Bocconi University as we way to pair incoming freshman with upperclassmen, with the objective of increasing the student retention rate.

```
$ python mentor_match.py --help
usage: mentor_match.py [-h] --mentors MENTORS --mentees MENTEES

Pairs mentees with a best fit mentor.

optional arguments:
  -h, --help         show this help message and exit

required named arguments:
  --mentors MENTORS  Filepath to the csv file with mentors to process.
  --mentees MENTEES  Filepath to the csv file with mentees to process.
```

## Input
Mentor and mentee data collected using a questionnaire (via Google Forms, Survey Monkey, etc.) then saved as a csv file and served as input to the script. The only mandatory fields for the csv are `NAME`, `SURNAME`, and `EMAIL`. The matching is based on any remaining fields in the file. 

## Output
The script will create two files:
- `matches.csv` will have all matches along with their data (match rate, question responses)
- `unmatched.csv` will have any mentees or mentors that did not receive a match

## Testing
If you care to give this a try, you can create some `.csv` files populated with random data by running `python ./tests/create_fixtures.py`. 