import os
import click
from tinydb import TinyDB, Query
from pathlib import Path
import os.path
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.tokenize import word_tokenize
import re
import textract
import json
import multiprocessing as mp

URL_DB_LOCATION = "/src/url.json"
URL_TEXT_LOCATION = "/src/url.txt"
FILE_LOCATION = '/data/aggregated/{0}'
TOKEN_FILE = '/data/token/{0}.tok'

# Available status
# 0. if it isn't process
# 1. if it was process but fails
# 2. if it was tokenized successfully
# 3. if it was count successfully


@click.command()
@click.option('--restart', default=False, type=bool,  help='Restart the tokenizer process.')
def main(restart):
    """Simple program that tokenize file information."""

    if restart:
        print("Starting a new tokenizer process...")
        os.remove(URL_DB_LOCATION)
        Path(URL_DB_LOCATION).touch()

        upload_db()
    else:
        print("Continuing tokenizer process...")

    db = TinyDB(URL_DB_LOCATION)
    process(db)
    return


# Process the collection of documents
def process(db):
    while True:
        doc = db.search(Query()['status'] == 0)
        if len(doc) == 0:
            break

        output = mp.Queue()

        # define the number of threads
        thread = 100
        if len(doc) <= 100:
            thread = len(doc)

        processes = [mp.Process(target=tokenize, args=(output, doc[x])) for x in range(thread)]

        # Run processes
        for p in processes:
            p.start()

        # Exit the completed processes
        for p in processes:
            p.join()

        # Get process results from the output queue
        invalid = []
        valid = []
        for p in processes:
            file, s = output.get()
            if s == 1:
                invalid.append(file)
            elif s == 2:
                valid.append(file)
            else:
                print("Status {} no register".format(s))
                exit(1)

        if len(invalid) != 0:
            db.update({'status': 1}, Query()['file'].one_of(invalid))
            print("Updating {} invalid documents".format(len(invalid)))

        if len(valid) != 0:
            db.update({'status': 2}, Query()['file'].one_of(valid))
            print("Updating {} valid documents".format(len(valid)))

    return


# Tokenize each document
def tokenize(output, doc):
    path = FILE_LOCATION.format(doc['file'])
    print("Tokening document {0}".format(str(path)))

    loc = Path(path)
    if not loc.is_file():
        print("File {} not found, continuing...".format(path))
        update_status(output, doc, 1)
        return

    text = extract_text(output, doc, path)
    if len(text) == 0:
        print("Empty text found, continuing...")
        update_status(output, doc, 1)
        return

    tokens = word_tokenize(text)
    if len(tokens) == 0:
        print("Empty token found, continuing...")
        update_status(output, doc, 1)
        return

    cleaned_token = clean(tokens)
    if len(cleaned_token) == 0:
        print("Empty cleaned token found, continuing...")
        update_status(output, doc, 1)
        return

    save_token(output, cleaned_token, doc)

    return


def save_token(output, cleaned_token, doc):
    token_file = TOKEN_FILE.format(doc['file'].split(".")[0])

    # remove if exists
    loc = Path(token_file)
    if loc.exists():
        os.remove(token_file)

    # create file for tokens
    Path(token_file).touch()

    # save tokens
    with open(token_file, 'w') as f:
        for token in cleaned_token:
            f.write("%s\n" % token)
        f.close()

    print("Saving tokens, continuing...")
    update_status(output, doc, 2)
    return


# Clean the token list
def clean(tokens):
    clean_tokens = []
    pattern = re.compile("^[0-9a-zA-Z]+$")
    only_number_pattern = re.compile("^[0-9]+$")
    for t in tokens:
        if not pattern.match(t):
            continue

        if only_number_pattern.match(t):
            continue

        t = t.lower()

        # Add other data cleaning

        clean_tokens.append(t)

    return clean_tokens


# Extract the text content from each file
def extract_text(output, doc, path):
    content_type = doc['content-type']

    if content_type == "text/plain":
        content = open_simple(output, doc, path)
        if len(content) == 0:
            return ""
        return content

    if content_type == "text/html":
        content = open_simple(output, doc, path)
        if len(content) == 0:
            return ""

        return extract_from_html(content)

    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or  \
            content_type == "application/msword" or \
            content_type == "application/pdf":
        content = open_complex(output, doc, path)
        if len(content) == 0:
            return ""

        return content
    else:
        print("Extraction for content type {0} no implemented".format(content_type))
        return ""

    return ""


# Open a complex file
def open_complex(output, doc, path):
    try:
        content = textract.process(path, encoding='unicode_escape')
        if len(content) == 0:
            print("No complex content found, continuing...")
            update_status(output, doc, 1)
            return ""
        return content.decode('unicode-escape')
    except:
        print("An exception occurred")
        return ""


# Open a simple file
def open_simple(output, doc, path):
    try:
        f = open(path, 'rb')
        content = f.read()
        f.close()
        if len(content) == 0:
            print("No text content found, continuing...")
            update_status(output, doc, 1)
            return ""

        return content.decode('unicode-escape')
    except:
        print("An exception occurred")
        return ""


# Extract the text from html files
def extract_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


# Update the status of each file execution
def update_status(output, doc, s):
    output.put((doc['file'], s))


# Load the url information into the .json data base
def upload_db():
    print("Creating url database file(this will take some minutes)...")
    with open(URL_TEXT_LOCATION) as fp:
        count = 1
        storage = {"_default": {}}

        for line in fp:
            info = line.split(";")
            file = info[2].replace("\n", "")
            storage["_default"][str(count)] = {
                "url": info[0],
                "content-type": info[1],
                "file": file,
                "status": 0,
                "number": int(file.split(".")[0])
            }
            print("Processing document {0}".format(info[2].replace("\n", "")))
            count += 1
        fp.close()

        f = open(URL_DB_LOCATION, "w")
        f.write(json.dumps(storage))
        f.close()


if __name__ == "__main__":
    main()
