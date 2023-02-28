import requests
import json
import time
import os

COUPON_URL = 'https://coupon-front.line.games/sbc/DC/useGameCoupon'
COUPON_FILE = 'coupons.txt'
USER_FILE = 'user.txt'
couponNos = [
    'demonfiesta', 'areyouready', 'collect', 'Golddungeon', 'destiny', 'child', 'premium', 'mileage', 'event', 'shop', 'racechallenge', 'Endlessduel', 'Devilrumble', 'Popupstore',
    'Worldmap', 'Worldboss', 'Community', 'Notice', 'Live2D', 'Mailbox', 'Labyrinth', 'Level', 'Devilpass', 'Ignition',
    'myroom', 'soulcarta', 'puppet', 'underground', 'completebonus', 'onair', 'rank', 'engarde', 'fullauto', 'Leader',
    'Party', 'reward', 'bloodgem', 'normal', 'hard', 'worldbattle', 'Gold', 'bronze', 'collectionpoint', 'exploration',
    'frontier', 'expert', 'unlimited', 'Exp', 'hottime', 'league', 'adventureofeve', 'scarletcollection', 'Spalocker',
    'gamestart', 'trialready', 'pvp', 'pve', 'comingsoon', 'worldbossrank', 'Max', 'mrs', 'rookie', 'ruby', 'common',
    'rare', 'Epic', 'legendary', 'material', 'convert', 'on', 'off', 'getreward', 'fever', 'summonchild', 'iteminventory',
    'class', 'uncommon', 'min', 'unknown', 'puppetdiorama', 'character', 'nebulalist', 'story', 'bgm', 'select',
    'reasonable', 'support', 'today', 'leaderbuff', 'easy', 'tier', 'Ragnaburst', 'Lanfeisshop', 'score', 'massivewar',
    'platinum', 'rumblemission', 'bursters', 'difficulty', 'dailyreward', 'sliver', 'weakpoint', 'puellaemagicae',
    'atonement', 'touchthescreen', 'drivecrush', 'Omen', 'rebirthmission', 'mainmission', 'manual', 'evil',
    'hecateslibrary', 'update', 'hp', 'ragnarank', 'summoncarta', 'slayersraid', 'slayercount', 'silver', 'rival',
    'bosslevel', 'raidshop', 'breakagain', 'Ragnabreaklimited', 'missionpass'
]
HEADERS = {
    'authority': 'coupon-front.line.games',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'JSESSIONID=B01508B6F052CBB35BCAA8A05B0DD8E1',
    'origin': 'https://coupon-front.line.games',
    'referer': 'https://coupon-front.line.games/sbc/DC',
    'sec-ch-ua': '"Whale";v="3", "Not-A.Brand";v="8", "Chromium";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

failed_coupons = []

def read_coupon_file():
    """
    If 'coupons.txt' file exists, read the contents and return as list.
    Otherwise, return an empty list.
    """
    coupon_list = []
    if os.path.exists(COUPON_FILE):
        with open(COUPON_FILE, 'r') as f:
            coupon_list = f.read().splitlines()
    return coupon_list

def use_coupon(userNo, couponNo):
    """
    Use the given coupon for the given user number.
    """
    data = {'userNo': userNo, 'couponNo': couponNo}
    try:
        response = requests.post(COUPON_URL, headers=HEADERS, data=data)
        response.raise_for_status()
        response_dict = json.loads(response.text)
        if response_dict.get('isSuccess'):
            print(f"{couponNo} - {response.text}")
        elif response_dict.get('errorCdStr') == 'FAIL_MAX_TRY_OVER':
            print(f"{couponNo} - {response.text}")
            time.sleep(10)
            response = requests.post(COUPON_URL, headers=HEADERS, data=data)
            response.raise_for_status()
            response_dict2 = json.loads(response.text)
            if not response_dict2.get('isSuccess'):
                failed_coupons.append(couponNo)
            print(f"{couponNo} - {response.text}")
        else:
            print(f"{couponNo} - {response.text}")
    except requests.exceptions.RequestException as e:
        failed_coupons.append(couponNo)
        print(e)


def write_failed_coupon_file(failed_coupons):
    """
    Write the failed coupons to the 'coupons.txt' file.
    """
    with open(COUPON_FILE, "w") as f:
        for couponNo in failed_coupons:
            f.write(couponNo + "\n")
    print("I saved the failed coupons to [coupon.txt]")


if __name__ == '__main__':
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            user_no = f.read()
            print(f"User number : {user_no}")
    else:
        user_no = input("Enter your user number (e.g., s6u834ase74b) [enter to exit]: ")
        with open(USER_FILE, "a") as f:
            f.write(user_no)
    if user_no == "":
        exit()

    coupon_list = read_coupon_file()
    if len(coupon_list):
        couponNos = coupon_list
        print("Read from coupon.txt and use it.")
    for couponNo in couponNos:
        use_coupon(user_no, couponNo)
        time.sleep(5)
    write_failed_coupon_file(failed_coupons)
    time.sleep(600)
