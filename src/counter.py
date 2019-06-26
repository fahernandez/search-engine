import click
import os
from pathlib import Path
import csv
import collections

COUNT_LOCATION = "/src/count.txt"
TOKEN_LOCATION = '/data/token/'
TOKEN_FILE = '/data/token/{}'


# Available status
# 0. if it isn't process
# 1. if it was process but fails
# 2. if it was process successfully


@click.command()
@click.option('--restart', default=False, type=bool,  help='Restart the count process.')
def main(restart):
    """Simple program that count the token information."""

    # restart and control files
    os.remove(COUNT_LOCATION)
    Path(COUNT_LOCATION).touch()

    # get token structure
    all_token = get_token_structure()
    # count the tokens
    counter = count(all_token)

    # Save the token result
    save(counter)
    return


# save the token information sorted by the count on appearance
def save(counter):
    print("Saving token information...")
    token_ordered = counter.most_common()
    with open(COUNT_LOCATION, 'w') as fp:
        fp.write('\n'.join('%s;%s' % x for x in token_ordered))
    return


# Count the token in the documents
def count(all_token):
    print("Counting token information...")
    return collections.Counter(all_token)


# Load all the token from the files
def get_token_structure():
    all_token = list()
    for filename in os.listdir(TOKEN_LOCATION):
        t = list()
        with open(TOKEN_FILE.format(filename), 'r') as fp:
            for line in fp:
                t.append(line.replace("\n", ""))
            fp.close()

        print("Processing file {0} with {1} tokens".format(filename, len(t)))
        all_token.extend(t)

    all_token.sort()
    print("Available {} tokens".format(len(all_token)))
    return all_token


if __name__ == "__main__":
    main()
