import requests
from bs4 import BeautifulSoup
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# dwBuildNumber -> Vergilius URL
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


def extract_offsets(url):
    offsets = {
        "Protection": None,
        "UniqueProcessId": None,
        "ActiveProcessLinks": None,
    }

    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return offsets

    soup = BeautifulSoup(r.text, "html.parser")

    for code in soup.find_all("code"):
        text = code.get_text()

        m = re.search(
            r"struct\s+_PS_PROTECTION\s+Protection\s*;.*?(0x[0-9a-fA-F]+)",
            text
        )
        if m:
            offsets["Protection"] = m.group(1)

        m = re.search(
            r"VOID\s*\*\s*UniqueProcessId\s*;.*?(0x[0-9a-fA-F]+)",
            text
        )
        if m:
            offsets["UniqueProcessId"] = m.group(1)

        m = re.search(
            r"struct\s+_LIST_ENTRY\s+ActiveProcessLinks\s*;.*?(0x[0-9a-fA-F]+)",
            text
        )
        if m:
            offsets["ActiveProcessLinks"] = m.group(1)

    return offsets


def main():
    prot_lines = []
    proc_lines = []
    first = True

    for build in sorted(TARGETS.keys()):
        offsets = extract_offsets(TARGETS[build])

        prot = offsets["Protection"]
        pid  = offsets["UniqueProcessId"]
        apl  = offsets["ActiveProcessLinks"]

        print(
            f"build = {build}, "
            f"0xProtection = {prot or 'NOT_PRESENT'}, "
            f"UniqueProcessId = {pid or 'NOT_PRESENT'}, "
            f"ActiveProcessLinks = {apl or 'NOT_PRESENT'}"
        )

        cond = "if" if first else "else if"
        first = False

        # ---- ProtectionOffset.txt ----
        prot_lines.append(
            f'{cond} (versionInfo.dwBuildNumber == {build}) {{\n'
            f'    OxProtection = {prot if prot else "0"};\n'
            f'}}'
        )

        # ---- ProcessOffsets.txt ----
        proc_lines.append(
            f'{cond} (versionInfo.dwBuildNumber == {build}) {{\n'
            f'    myOffsets.uniqueProcessIDOffset = {pid if pid else "0"};\n'
            f'    myOffsets.ActiveProcessLinkOffset = {apl if apl else "0"};\n'
            f'}}'
        )

        time.sleep(1)

    prot_lines.append("else {\n    OxProtection = 0;\n}")
    proc_lines.append(
        "else {\n"
        "    myOffsets.uniqueProcessIDOffset = 0;\n"
        "    myOffsets.ActiveProcessLinkOffset = 0;\n"
        "}"
    )

    with open("ProtectionOffset.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(prot_lines))

    with open("ProcessOffsets.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(proc_lines))

    print("\n[+] Generated ProtectionOffset.txt")
    print("[+] Generated ProcessOffsets.txt")


if __name__ == "__main__":
    main()
