from gddecoder import decoders
from getpass import getuser
import re
import sys


def main():

    path = f"C:\\Users\\{getuser()}\\AppData\\Local\\GeometryDash\\"
    if len(sys.argv) == 2:
        path = sys.argv[1]

    try:
        print("Read Manager...")
        with open(path + "CCGameManager.dat", "rb") as fp:
            manager = fp.read()
    except FileNotFoundError:
        print(f"Error: Files 'CCGameManager.dat' not found at '{path}'")
        return

    mdata = decoders.save_file_decoder(manager)

    print("Name and password extract...")
    username = re.search(r"<k>GJA_001<\/k><s>([\d+\w+ ]+)<\/s>", mdata).group(1)
    password = re.search(r"<k>GJA_002<\/k><s>([\d+\w+-]+)<\/s>", mdata).group(1)

    print("Username:", username)
    print("Password:", password)

    print("Successful")


if __name__ == '__main__':
    print("Password extractor by LordNodus")
    try:
        main()
    except Exception as err:
        with open("log.txt", "a") as fp:
            fp.write(str(err) + "\n")
    input("Enter to exit")

