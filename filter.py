import json
import argparse
import re
import subprocess

import pandas as pd

BASE_COMMAND=["python3", "-m", "autograder.run.peek"]

def main():
    parser = argparse.ArgumentParser("splendor")
    parser.add_argument("filename")
    parser.add_argument('-t', "--threshold", default=0.85,
                        help="Minimum mean similarity to flag pairs", type=float)
    parser.add_argument('-c', "--config",
                        help="Config file for autograder", type=str)

    args = parser.parse_args()

    if args.threshold > 1 or args.threshold < 0:
        raise ValueError("Threshold value must be between 0 and 1")

    with open(args.filename, 'r') as f:
        data = json.load(f)
   
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        config = None

    results = data['results']
    flagged_comparisons = []

    for pair in results:
        if pair.get('total-mean-similarity', 0) >= args.threshold:
            concern = f"{int(pair['total-mean-similarity'] * 100)}% similarity"

            email_1, id_1 = get_email_and_id(pair['submission-ids'][0])
            email_2, _ = get_email_and_id(pair['submission-ids'][1])

            score = get_score(email_1, id_1, config)

            flagged_comparisons.append({
                "email_1": email_1,
                "email_2": email_2,
                "concern": concern,
                "score": score
            })

    df = pd.DataFrame(flagged_comparisons)
    csv_str = df.to_csv(index=False)
    print(csv_str)

def get_score(email, id, config=None):
    """Run bash commands to retrieve score of submission given email and id"""

    # if the config is provided, then we pass the config arguments into the command line.
    # if the config is not provided, it is assumed to be in the present directory.
    # thus, we don't pass any additional arguments and let the autograder cli read them itself.
    if config:
        command = BASE_COMMAND + ["--server", config["server"], "--course", config["course"],
                                  "--assignment", config["assignment"], 
                                  "--user", config["user"], "--pass", config["pass"],
                                  "--target-email", email,  "--target-submission", id]
    else:
        command = BASE_COMMAND + ["--target-email", email,  "--target-submission", id]

    process = subprocess.run(command, capture_output=True, text=True)
    
    process.check_returncode()

    pattern = r"Total: (\d+ / \d+)"
    match = re.findall(pattern, process.stdout)

    if not match:
        raise ValueError("No score found in output", process.stdout)
    return match[0]

def get_email_and_id(raw_submission_id):
    """
    Convert submission-id into email and numeric id.

    ex: "cse40-s25::ho3::examplestudent@ucsc.edu::123456789" -> (examplestudent@ucsc.edu, 123456789)
    """

    pattern = r"::.+::(.+@ucsc.edu)::(\d+)"
    match = re.findall(pattern, raw_submission_id)

    if not match:
        raise ValueError("No email or id found in submission-id", raw_submission_id)
    if len(match[0]) != 2:
        raise ValueError("Multiple emails or ids found in submission-id", id)

    return match[0]
    

if __name__=="__main__":
    main()
