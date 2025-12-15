
# 0xProtectOffsetScrapper

A small **Python utility** to scrape the **`EPROCESS → Protection` offset** (`_PS_PROTECTION`) from  
👉 **https://www.vergiliusproject.com**

This has been **vibe coded for my own ease** to quickly pull the `0xProtection` offset across multiple Windows versions and builds without manually browsing kernel structure pages.

> Huge shout-out to **Vergilius Project** — their work is awesome.  
> Please do visit and support them: **https://www.vergiliusproject.com**

---

## 🔍 What this does

- Scrapes `_EPROCESS` structure pages from **Vergilius Project**
- Extracts the offset for:
  ```c
  struct _PS_PROTECTION Protection;

* Outputs results in a **ready-to-use format**:

  ```text
  build = 19041, 0xProtection = 0x87a
  ```
* Uses **authoritative `dwBuildNumber` mappings**
* Covers:

  * Windows 8 / 8.1
  * Windows 10 (1507 → 22H2)
  * Windows 11 (21H2 → 25H2)
  * Windows Server 2022

---

## 🧠 Why this exists

When doing **kernel research, reversing, red-team labs, or driver analysis**, you often need:

* The correct `EPROCESS.Protection` offset
* Mapped to the **real kernel build number (`dwBuildNumber`)**
* Without guessing marketing versions or manually clicking pages

This script automates that lookup using **Vergilius as a reference source**.

---

## ⚙️ How it works

1. Uses a predefined mapping of:

   ```text
   dwBuildNumber → Vergilius _EPROCESS URL
   ```
2. Fetches the `_EPROCESS` page
3. Matches this exact declaration:

   ```c
   struct _PS_PROTECTION Protection;
   ```
4. Extracts the hex offset from the same line
5. Prints normalized output

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

### Example output

```text
build = 17763, 0xProtection = 0x6fa
build = 18362, 0xProtection = 0x6fa
build = 19041, 0xProtection = 0x87a
build = 20348, 0xProtection = 0x87a
build = 22621, 0xProtection = 0x87a
```

If a build does not contain `_PS_PROTECTION`, the output will be:

```text
build = 14393, 0xProtection = NOT_PRESENT
```

---

## ⚠️ Important notes

* **Vergilius is a reference**, not a guarantee
* Offsets **can change** due to:

  * Cumulative updates
  * Insider builds
  * Kernel layout changes
* Always **verify offsets using symbols** for real tooling:

  ```text
  dt nt!_EPROCESS Protection
  ```

This project is intended for:

* Learning
* Research
* Labs
* Reverse engineering
* Automation convenience

**Do not blindly hardcode offsets in production code.**

---

## ❤️ Credits

All kernel structure data comes from:

👉 **Vergilius Project**
[https://www.vergiliusproject.com](https://www.vergiliusproject.com)

Their work makes Windows internals research significantly easier — please support them.

---

## 📜 License

This project is provided **as-is** for educational and research purposes.
Use responsibly.


