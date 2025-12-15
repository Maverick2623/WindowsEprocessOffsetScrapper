import requests
from bs4 import BeautifulSoup
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Authoritative URL → dwBuildNumber mapping (from your table)
TARGETS = {
    26200: "https://www.vergiliusproject.com/kernels/x64/windows-11/25h2/_EPROCESS",
    26100: "https://www.vergiliusproject.com/kernels/x64/windows-11/24h2/_EPROCESS",
    22631: "https://www.vergiliusproject.com/kernels/x64/windows-11/23h2/_EPROCESS",
    22621: "https://www.vergiliusproject.com/kernels/x64/windows-11/22h2/_EPROCESS",
    22000: "https://www.vergiliusproject.com/kernels/x64/windows-11/21h2/_EPROCESS",
    20348: "https://www.vergiliusproject.com/kernels/x64/server-2022/21h2/_EPROCESS",

    19045: "https://www.vergiliusproject.com/kernels/x64/windows-10/22h2/_EPROCESS",
    19044: "https://www.vergiliusproject.com/kernels/x64/windows-10/21h2/_EPROCESS",
    19043: "https://www.vergiliusproject.com/kernels/x64/windows-10/21h1/_EPROCESS",
    19042: "https://www.vergiliusproject.com/kernels/x64/windows-10/20h2/_EPROCESS",
    19041: "https://www.vergiliusproject.com/kernels/x64/windows-10/2004/_EPROCESS",

    # 1903 / 1909 share kernel layout
    18362: "https://www.vergiliusproject.com/kernels/x64/windows-10/1903/_EPROCESS",

    17763: "https://www.vergiliusproject.com/kernels/x64/windows-10/1809/_EPROCESS",
    17134: "https://www.vergiliusproject.com/kernels/x64/windows-10/1803/_EPROCESS",
    16299: "https://www.vergiliusproject.com/kernels/x64/windows-10/1709/_EPROCESS",
    15063: "https://www.vergiliusproject.com/kernels/x64/windows-10/1703/_EPROCESS",
    14393: "https://www.vergiliusproject.com/kernels/x64/windows-10/1607/_EPROCESS",
    10586: "https://www.vergiliusproject.com/kernels/x64/windows-10/1511/_EPROCESS",
    10240: "https://www.vergiliusproject.com/kernels/x64/windows-10/1507/_EPROCESS",

    9600:  "https://www.vergiliusproject.com/kernels/x64/windows-8.1/update-1/_EPROCESS",
    9200:  "https://www.vergiliusproject.com/kernels/x64/windows-8/rtm/_EPROCESS",
}

def extract_protection_offset(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    for code in soup.find_all("code"):
        text = code.get_text()

        # Match:
        # struct _PS_PROTECTION Protection;  // 0x87a
        match = re.search(
            r"struct\s+_PS_PROTECTION\s+Protection\s*;.*?(0x[0-9a-fA-F]+)",
            text
        )
        if match:
            return match.group(1)

    return None


def main():
    for build in sorted(TARGETS.keys()):
        url = TARGETS[build]
        offset = extract_protection_offset(url)

        if offset:
            print(f"build = {build}, 0xProtection = {offset}")
        else:
            print(f"build = {build}, 0xProtection = NOT_PRESENT")

        time.sleep(1)


if __name__ == "__main__":
    main()
