from gddecoder import decoders
from getpass import getuser
import re
import sys
import aiohttp
import asyncio


async def requests(data, header):
    async with aiohttp.request("POST", "http://www.boomlings.com/database/accounts/loginGJAccount.php",
                               data=data, headers=header,
                               skip_auto_headers=["User-Agent", "Accept-Encoding"]) as req:
        return req.status, await req.text()


def main():

    username = input("Enter user name: ")
    password = input("Enter password: ")

    path = f"C:\\Users\\{getuser()}\\AppData\\Local\\GeometryDash\\"
    if len(sys.argv) == 2:
        path = sys.argv[1]

    try:
        print("Opening manager...")
        with open(path + "CCGameManager.dat", "rb") as fp:
            manager_data = fp.read()
    except FileNotFoundError:
        print(f"Error: file '{path}CCGameManager.dat' cannot be created")
        return

    print("Decoding...")
    manager = decoders.save_file_decoder(manager_data)

    print("Extracting udid...")
    udid = re.search(r"<k>playerUDID<\/k><s>([\d+\w+-]+)<\/s>", manager).group(1)

    data = {
        "udid": udid,
        "userName": username,
        "password": password,
        "secret": "Wmfv3899gc9",
    }
    header = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Loading data...")
    status, text_data = asyncio.run(requests(data, header))

    if status != 200:
        print("Error: code", status, "\nResponse:")
        print(text_data)
        return

    if text_data == "-1":
        print("Error: account information is incorrect")
        return

    print("Unpacking...")
    try:
        accountID, playerID = text_data.split(",")
    except Exception:
        print("Error: data can't unpack")
        return

    print("Forming...")
    st1, st2 = re.split(r"<k>GJA_002<\/k><s>[\d+\w+-]+<\/s>", manager, 1)
    manager = st1 + f"<k>GJA_002</k><s>{password}</s>" + st2

    st1, st2 = re.split(r"<k>GJA_003<\/k><i>\d+<\/i>", manager, 1)
    manager = st1 + f"<k>GJA_003</k><i>{accountID}</i>" + st2

    st1, st2 = re.split(r"<k>playerUserID<\/k><i>\d+<\/i>", manager, 1)
    manager = st1 + f"<k>playerUserID</k><i>{playerID}</i>" + st2

    st1, st2 = re.split(r"<k>GJA_001<\/k><s>[\d\w ]+<\/s>", manager, 1)
    manager = st1 + f"<k>GJA_001</k><s>{username}</s>" + st2

    st1, st2 = re.split(r"<k>playerName<\/k><s>[\d\w ]+<\/s>", manager, 1)
    manager = st1 + f"<k>playerName</k><s>{username}</s>" + st2

    print("Encoding manager...")
    manager_data = decoders.save_file_encoder(manager)

    print("Save...")
    try:
        with open(path + "CCGameManager.dat", "wb") as fp:
            fp.write(manager_data)
    except FileNotFoundError:
        print(f"Error: file '{path}CCGameManager.dat' cannot be overwritten")
        return

    print("Successful")


if __name__ == '__main__':
    print("Data refresher by LordNodus")
    try:
        main()
    except Exception as err:
        with open("log.txt", "a") as fp:
            fp.write(str(err) + "\n")
    input("Enter to exit")
