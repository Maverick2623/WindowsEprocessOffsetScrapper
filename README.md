
# 0xProtectOffsetScrapper

A small **Python utility** to scrape **`EPROCESS` offsets** from  
👉 **https://www.vergiliusproject.com**

This project has been **vibe coded for my own ease** to quickly extract commonly used
`EPROCESS` offsets across Windows versions and kernel builds, without manually browsing
kernel structure pages.

> Huge shout-out to **Vergilius Project** — their work is awesome.  
> Please do visit and support them: **https://www.vergiliusproject.com**

---

## 🔍 What this tool does

- Scrapes `_EPROCESS` structure pages from **Vergilius Project**
- Extracts the following offsets:
  ```c
  struct _PS_PROTECTION Protection;
  VOID* UniqueProcessId;
  struct _LIST_ENTRY ActiveProcessLinks;


* Prints results on-screen per build
* Generates **ready-to-paste C/C++ resolver code** into separate files
* Uses **real kernel build numbers (`dwBuildNumber`)**
* Covers:

  * Windows 8 / 8.1
  * Windows 10 (1507 → 22H2)
  * Windows 11 (21H2 → 25H2)
  * Windows Server 2022

---

## 🧠 Why this exists

When doing **kernel research, driver auditing, red-team labs, BYOVD analysis, or EDR research**, you often need:

* Accurate `EPROCESS` offsets
* Mapped to the **actual kernel build number**
* In a form that can be **directly pasted into C/C++ code**

This script automates that process using **Vergilius as a reference source** and produces
both human-readable output and copy-paste-ready logic.

---

## ⚙️ How it works

1. Uses an authoritative mapping of:

   ```text
   dwBuildNumber → Vergilius _EPROCESS URL
   ```
2. Fetches the `_EPROCESS` page
3. Matches exact struct declarations
4. Extracts the hex offsets
5. Produces:

   * Console output
   * `ProtectionOffset.txt`
   * `ProcessOffsets.txt`

---

## 📦 Requirements

* Python **3.8+**
* Dependencies:

  ```bash
  pip install requests beautifulsoup4
  ```

---

## ▶️ Usage

```bash
python scraper.py
```

---

## 🖥️ Console output example

```text
build = 17763, 0xProtection = 0x6fa, UniqueProcessId = 0x440, ActiveProcessLinks = 0x448
```

If a field does not exist in a build:

```text
build = 14393, 0xProtection = NOT_PRESENT, UniqueProcessId = 0x2e0, ActiveProcessLinks = 0x2e8
```

---

## 📄 Generated files

### 1️⃣ `ProtectionOffset.txt`

Contains **only Protection offset logic**, suitable for PPL / protection checks.

```cpp
if (versionInfo.dwBuildNumber == 9200) {
    OxProtection = 0;
}
else if (versionInfo.dwBuildNumber == 9600) {
    OxProtection = 0x67a;
}
else {
    OxProtection = 0;
}
```

✔ Valid C/C++
✔ No syntax errors
✔ Safe fallback

---

### 2️⃣ `ProcessOffsets.txt`

Contains **process-walking related offsets**.

```cpp
if (versionInfo.dwBuildNumber == 9200) {
    myOffsets.uniqueProcessIDOffset = 0x2e0;
    myOffsets.ActiveProcessLinkOffset = 0x2e8;
}
else if (versionInfo.dwBuildNumber == 9600) {
    myOffsets.uniqueProcessIDOffset = 0x440;
    myOffsets.ActiveProcessLinkOffset = 0x448;
}
else {
    myOffsets.uniqueProcessIDOffset = 0;
    myOffsets.ActiveProcessLinkOffset = 0;
}
```

✔ Ready for EPROCESS traversal
✔ Clean separation of concerns
✔ Copy-paste safe

---

## ⚠️ Important notes

* **Vergilius is a reference**, not a guarantee
* Offsets **can change** due to:

  * Cumulative updates
  * Insider builds
  * Kernel layout changes
* Always **verify offsets with symbols** when building real tooling:

  ```text
  dt nt!_EPROCESS
  ```

This project is intended for:

* Learning
* Research
* Reverse engineering
* Red-team labs
* Automation convenience

⚠️ **Do not blindly hardcode offsets in production code.**

---

## ❤️ Credits

All kernel structure data comes from:

👉 **Vergilius Project**
[https://www.vergiliusproject.com](https://www.vergiliusproject.com)

Their work makes Windows internals research significantly easier — please support them.

---

## 📜 License

This project is licensed under the **MIT License**.
