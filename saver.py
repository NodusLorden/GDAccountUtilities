from gddecoder import decoders
from getpass import getuser
import re
import sys
import aiohttp
import asyncio


async def requests(data, header):
    async with aiohttp.request("POST", "http://www.robtopgames.net/database/accounts/backupGJAccountNew.php",
                               data=data, headers=header, expect100=True,
                               skip_auto_headers=["User-Agent", "Accept-Encoding"]) as req:
        return req.status, await req.text()


def main():

    path = f"C:\\Users\\{getuser()}\\AppData\\Local\\GeometryDash\\"
    if len(sys.argv) == 2:
        path = sys.argv[1]

    try:
        print("Read Manager...")
        with open(path + "CCGameManager.dat", "rb") as fp:
            manager = fp.read()

        print("Read Levels...")
        with open(path + "CCLocalLevels.dat", "rb") as fp:
            levels = fp.read()

    except FileNotFoundError:
        print(f"Error: Files 'CCGameManager.dat' or 'CCLocalLevels.dat' not found at '{path}'")
        return

    print("Decoding manager...")
    mdata = decoders.save_file_decoder(manager)

    print("Extracting name and password...")
    username = re.search(r"<k>GJA_001<\/k><s>([\d+\w+ ]+)<\/s>", mdata).group(1)
    password = re.search(r"<k>GJA_002<\/k><s>([\d+\w+-]+)<\/s>", mdata).group(1)

    print("Converting data...")
    xmamager = decoders.xor(manager).decode().strip("\0")
    xlevels = decoders.xor(levels).decode().strip("\0")
    game_data = xmamager + ";" + xlevels

    print("Build request...")
    data = {
        "userName": username,
        "password": password,
        "gameVersion": "21",
        "binaryVersion": 35,
        "gdw": 0,
        "saveData": game_data,
        "secret": "Wmfv3899gc9",
    }
    header = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Data size", round(len(game_data) / 2**10, 3), "kb")
    print("Levels size", round(len(xlevels) / 2**10, 3), "kb")

    if len(xlevels) > 2**20 * 32:
        print("Warning: Levels size more 32mb")

    print("Loading data...")
    status, text_data = asyncio.run(requests(data, header))

    if status != 200:
        print("Error: code", status, "\nResponse:")
        print(text_data)
        return

    if text_data == "-5":
        print("Error: account information is incorrect")
        return

    print("Successful")


if __name__ == '__main__':
    print("Account saver by LordNodus")
    try:
        main()
    except Exception as err:
        with open("log.txt", "a") as fp:
            fp.write(str(err) + "\n")
    input("Enter to exit")
