# Pairwise-Comparison-Filter
This program will scan a JSON file made with the autograder and find all instances
of pairs that have higher similarity than the given threshold (default 0.85). 

It will output the pairs in a csv format that can be pasted into a spreadsheet.To split the output into multiple columns in Google Sheets, go to Data > Split Text to Columns.

## Usage
Run the command `python3 filter.py` with the following arguments to run the program.

```
usage: python3 filter.py [-h] [-t THRESHOLD] [-c CONFIG] filename

positional arguments:
  filename              JSON file to check for pairwise similarity

options:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        Minimum mean similarity to flag pairs
  -c CONFIG, --config CONFIG
                        Config file for autograder. If no config file is provided then 
                        it is assumed that there is a config file in the present working directory.   
```

The config file should have the same format as the autograder.

