from gddecoder import decoders
from getpass import getuser
import re
import sys
import aiohttp
import asyncio


async def requests(data, header):
    async with aiohttp.request("POST", "http://www.robtopgames.net/database/accounts/syncGJAccountNew.php",
                               data=data, headers=header,
                               skip_auto_headers=["User-Agent", "Accept-Encoding"]) as req:
        return req.status, await req.text()


def main():

    path = f"C:\\Users\\{getuser()}\\AppData\\Local\\GeometryDash\\"
    if len(sys.argv) == 2:
        path = sys.argv[1]

    username = input("Enter user name: ")
    password = input("Enter password: ")

    data = {
        "userName": username,
        "password": password,
        "secret": "Wmfv3899gc9",
        "gameVersion": "21",
        "binaryVersion": 35,
        "gdw": 0,
    }
    header = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Loading data...")
    status, text_data = asyncio.run(requests(data, header))

    if status != 200:
        print("Error: code", status, "\nResponse:")
        print(text_data)
        return

    if text_data == "-11" or "-1":
        print("Error: account information is incorrect")
        return

    print("Unpacking...")
    try:
        manager, levels, key, build, *other = text_data.split(";")
    except Exception:
        print("Error: data can't unpack")
        return

    print("Injecting data...")
    string_data = decoders.from_gzip(decoders.from_base64(manager.encode()))
    st1, st2 = re.split(r"<k>GJA_002<\/k><s>[\d+\w+-]+<\/s>", string_data, 1)
    string_data = st1 + f"<k>GJA_002</k><s>{password}</s>" + st2

    print("Encoding manager...")
    manager_data = decoders.save_file_encoder(string_data)

    print("Converting levels...")
    level_data = decoders.xor(levels.encode())

    print("Save...")
    try:
        with open(path + "CCGameManager.dat", "wb") as fp:
            fp.write(manager_data)
        with open(path + "CCLocalLevels.dat", "wb") as fp:
            fp.write(level_data)
    except FileNotFoundError:
        print(f"Error: file '{path}CCGameManager.dat' or '{path}CCLocalLevels.dat' cannot be created")
        return

    print("Successful")


if __name__ == '__main__':
    print("Loginer by LordNodus")
    try:
        main()
    except Exception as err:
        with open("log.txt", "a") as fp:
            fp.write(str(err) + "\n")
    input("Enter to exit")
