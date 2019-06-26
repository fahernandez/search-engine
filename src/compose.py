import os
import click
from pathlib import Path
from shutil import copyfile
from pathlib import Path
import csv
import magic
import urllib.parse
import glob

CLASSMATES_DATA_LOCATION = "/data/classmates/{}"
AGGREGATED_DATA_LOCATION = "/data/aggregated/{}"
URL_TEXT_LOCATION = "/src/url.txt"

EXTENSIONS = {
    "text/html": "{}.html",
    "application/pdf": "{}.pdf",
    "text/plain": "{}.txt",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "{}.docx",
    "text/xml": "{}.xml",
    "application/xml": "{}.xml",
    "application/msword": "{}.doc",
    "application/octet-stream": "{}.doc",
}

EXTENSIONS_IGNORE = {
    "image/png": "{}.png",
    "image/jpeg": "{}.jpg",
    "text/x-python": "{}.py",
    "inode/x-empty": "{}.py",
    "text/x-c++": "{}.py",
    "application/x-wine-extension-ini": "{}.ini",
    "application/x-gzip": "{}.gzip",
}

FILE_NUMBER = 1

@click.command()
@click.option('--restart', default=False, type=bool,  help='Restart the compose process.')
def main(restart):
    """Simple program that compose data from classmates information."""

    print("Starting a new compose process...")
    os.remove(URL_TEXT_LOCATION)
    Path(URL_TEXT_LOCATION).touch()

    adrian_quiros()
    adrian_vargas()
    carlos_solis()
    daniel_herrera()
    deivert_guiltrichs()
    esteban_rodriguez()
    fabian_hernandez()
    mario_cabrera()
    michelle_cersosimo()
    pablo_calvo()

    return


def adrian_quiros():
    print("--------------Composing Adrian Quiros Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("AdrianQuiros/Coleccion/")
    url = CLASSMATES_DATA_LOCATION.format("AdrianQuiros/Urls.txt")

    count = 1
    with open(url) as fp:
        for line in fp:
            info = line.split(",")
            url = info[1]
            name = info[0]
            path = collection + name

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                count += 1
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                count += 1
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                count += 1
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                count += 1
                continue

        fp.close()


def adrian_vargas():
    print("--------------Composing Adrian Vargas Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("AdrianVargas/coleccion/")
    url = CLASSMATES_DATA_LOCATION.format("AdrianVargas/urls.txt")

    with open(url) as fp:
        for line in fp:
            info = line.split("_")
            name = info[0]
            url = info[1]
            path = collection + name

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                continue
        fp.close()


def carlos_solis():
    print("--------------Composing Carlos Solis Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("CarlosSolis/")
    url = CLASSMATES_DATA_LOCATION.format("CarlosSolis/urls.csv")

    count = 1
    with open(url) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            url = line[0]

            files = glob.glob("{}{}.*".format(collection, str(count)))
            if len(files) != 1:
                print("Ignored file {} ".format(str(count)))
                count += 1
                continue

            path = files[0]

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                count += 1
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                count += 1
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                count += 1
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                count += 1
                continue


def daniel_herrera():
    print("--------------Composing Daniel Herrera Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("DanielHerrera/")
    url = CLASSMATES_DATA_LOCATION.format("DanielHerrera/url.txt")

    count = 1
    with open(url) as fp:
        for line in fp:
            info = line.split(",")
            url = info[0]
            path = collection + str(count)

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                count += 1
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                count += 1
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                count += 1
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                count += 1
                continue

        fp.close()


def deivert_guiltrichs():
    print("--------------Composing Carlos Solis Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("DeivertGuiltrichs/contenido/")
    url = CLASSMATES_DATA_LOCATION.format("DeivertGuiltrichs/urls.txt")

    count = 0
    with open(url) as fp:
        for line in fp:
            info = line.split(",")
            url = info[0]
            ext = info[1].replace("\n", "")
            path = collection + str(count) + ext

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                count += 1
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                count += 1
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                count += 1
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                count += 1
                continue
        fp.close()


def esteban_rodriguez():
    print("--------------Composing Esteban Rodriguez Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("EstebanRodriguezBetancourt/entrega_crawl/")
    url = CLASSMATES_DATA_LOCATION.format("EstebanRodriguezBetancourt/entrega_crawl/documents.csv")

    count = 1
    with open(url) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            url = line[0]
            file = str(count)
            path = collection + file

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                count += 1
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                count += 1
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                count += 1
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                count += 1
                continue


def fabian_hernandez():
    print("--------------Composing Fabián Hernández Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("FabianHernandez/")
    url = CLASSMATES_DATA_LOCATION.format("FabianHernandez/url.txt")

    with open(url) as fp:
        for line in fp:
            info = line.split(",")
            url = info[0]
            file = info[2].replace("\n", "")
            path = collection + file

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                continue


def mario_cabrera():
    print("--------------Composing Mario Cabrera Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("MarioCabrera/collection/")
    url = CLASSMATES_DATA_LOCATION.format("MarioCabrera/urls.txt")

    count = 0
    with open(url) as fp:
        for line in fp:
            info = line.split(", ")
            url = info[0]
            content_type = info[1].replace("\n", "")

            if content_type in EXTENSIONS.keys():
                file = EXTENSIONS[content_type].format(count)
                path = collection + file

                loc = Path(path)
                if not loc.exists():
                    print("File {} is no valid".format(path))
                    count += 1
                    continue

                mime = magic.Magic(mime=True)
                content_type = mime.from_file(path)
                if content_type in EXTENSIONS_IGNORE.keys():
                    print("Content type {} is no valid".format(content_type))
                    count += 1
                    continue

                if content_type in EXTENSIONS.keys():
                    copy(url, path, content_type)
                    count += 1
                    continue
                else:
                    print("Extension {} no reviewed.".format(content_type))
                    count += 1
                    continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                count += 1
                continue

        fp.close()


def michelle_cersosimo():
    print("--------------Composing Michelle Cersosimo Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("MichelleCersosimo/Coleccion/")
    url = CLASSMATES_DATA_LOCATION.format("MichelleCersosimo/Coleccion/urls.txt")

    count = 1
    with open(url) as fp:
        for line in fp:
            info = line.split(",")
            url = info[0]
            almost = info[1].replace("\n", "").split(";")

            if len(almost) < 1:
                print(almost)
                exit(1)

            content_type = almost[0]
            if content_type in EXTENSIONS.keys():
                file = EXTENSIONS[content_type].format(count)
                path = collection + file

                loc = Path(path)
                if not loc.exists():
                    print("File {} is no valid".format(path))
                    count += 1
                    continue

                mime = magic.Magic(mime=True)
                content_type = mime.from_file(path)
                if content_type in EXTENSIONS_IGNORE.keys():
                    print("Content type {} is no valid".format(content_type))
                    count += 1
                    continue

                if content_type in EXTENSIONS.keys():
                    copy(url, path, content_type)
                    count += 1
                    continue
                else:
                    print("Extension {} no reviewed.".format(content_type))
                    count += 1
                    continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                count += 1
                continue

    fp.close()


def pablo_calvo():
    print("--------------Composing Pablo Calvo Files-------------------")
    collection = CLASSMATES_DATA_LOCATION.format("PauloCalvov2/")
    url = CLASSMATES_DATA_LOCATION.format("PauloCalvov2/linksGuardados.txt")

    mime = magic.Magic(mime=True)

    with open(url) as fp:
        for line in fp:
            info = line.split(",")
            url = info[1].replace("\n", "")
            file = info[0]
            path = collection + file

            loc = Path(path)
            if not loc.exists():
                print("File {} is no valid".format(path))
                continue

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(path)
            if content_type in EXTENSIONS_IGNORE.keys():
                print("Content type {} is no valid".format(content_type))
                continue

            if content_type in EXTENSIONS.keys():
                copy(url, path, content_type)
                continue
            else:
                print("Extension {} no reviewed.".format(content_type))
                continue

        fp.close()


# copy the file into the new location
def copy(url, path, content_type):
    global FILE_NUMBER

    loc = Path(path)
    if not loc.exists():
        print("File {} is no valid".format(path))
        exit(1)

    file_name = EXTENSIONS[content_type].format(FILE_NUMBER)

    writer = csv.writer(open(URL_TEXT_LOCATION, "a"), delimiter=';')
    writer.writerow([urllib.parse.quote_plus(url), content_type, file_name])

    copyfile(path, AGGREGATED_DATA_LOCATION.format(file_name))
    print("Copied file {} with number {}".format(path, FILE_NUMBER))
    FILE_NUMBER += 1


if __name__ == "__main__":
    main()
