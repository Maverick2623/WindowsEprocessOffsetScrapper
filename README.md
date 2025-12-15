Here’s the **updated `README.md` in Markdown**, reflecting the new **`code.txt` C/C++ code generation feature**, while keeping your original vibe and intent intact.

You can **copy-paste this directly** into `README.md`.

---


# 0xProtectOffsetScrapper

A small **Python utility** to scrape the **`EPROCESS → Protection` offset** (`_PS_PROTECTION`) from  
👉 **https://www.vergiliusproject.com**

This project has been **vibe coded for my own ease** to quickly pull the `0xProtection` offset across multiple Windows versions and kernel builds without manually browsing kernel structure pages.

> Huge shout-out to **Vergilius Project** — their work is awesome.  
> Please do visit and support them: **https://www.vergiliusproject.com**

---

## 🔍 What this tool does

- Scrapes `_EPROCESS` structure pages from **Vergilius Project**
- Extracts the offset for:
  ```c
  struct _PS_PROTECTION Protection;


* Prints results on-screen in a readable format
* **Generates ready-to-use C/C++ resolver code** in `code.txt`
* Uses **real `dwBuildNumber` values**, not marketing versions
* Covers:

  * Windows 8 / 8.1
  * Windows 10 (1507 → 22H2)
  * Windows 11 (21H2 → 25H2)
  * Windows Server 2022

---

## 🧠 Why this exists

When doing **kernel research, reversing, red-team labs, driver auditing, or BYOVD analysis**, you often need:

* The correct `EPROCESS.Protection` offset
* Mapped to the **actual kernel build number (`dwBuildNumber`)**
* In a form that can be **directly pasted into C/C++ code**

This script automates that process using **Vergilius as a reference source** and outputs both:

* Human-readable results
* Copy-paste-ready C/C++ logic

---

## ⚙️ How it works

1. Uses an authoritative mapping of:

   ```text
   dwBuildNumber → Vergilius _EPROCESS URL
   ```
2. Fetches the `_EPROCESS` page
3. Matches this exact declaration:

   ```c
   struct _PS_PROTECTION Protection;
   ```
4. Extracts the hex offset from the same line
5. Outputs:

   * Console results
   * A C/C++ `if / else if / else` resolver in `code.txt`

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
build = 17763, 0xProtection = 0x6fa
build = 18362, 0xProtection = 0x6fa
build = 19041, 0xProtection = 0x87a
build = 20348, 0xProtection = 0x87a
build = 22621, 0xProtection = 0x87a
```

If a build does not contain `_PS_PROTECTION`:

```text
build = 14393, 0xProtection = NOT_PRESENT
```

---

## 📄 Generated file: `code.txt`

The script automatically creates a file named **`code.txt`** containing **valid C/C++ code** that you can directly paste into your function.

### Example `code.txt`

```cpp
if (versionInfo.dwBuildNumber == 17763) {
    OxProtection = 0x6fa;
}
else if (versionInfo.dwBuildNumber == 18362) {
    OxProtection = 0x6fa;
}
else if (versionInfo.dwBuildNumber == 19041) {
    OxProtection = 0x87a;
}
else {
    OxProtection = 0;
}
```

### Guarantees

* ✅ No syntax errors
* ✅ Proper braces
* ✅ No duplicate `if`
* ✅ Safe fallback (`OxProtection = 0`)
* ✅ Ready for kernel or user-mode use

---

## ⚠️ Important notes

* **Vergilius is a reference**, not a guarantee
* Offsets **can change** due to:

  * Cumulative updates
  * Insider builds
  * Kernel layout changes
* Always **verify offsets with symbols** when building real tooling:

  ```text
  dt nt!_EPROCESS Protection
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
