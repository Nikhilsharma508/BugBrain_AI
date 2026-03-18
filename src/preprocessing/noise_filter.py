"""
src/preprocessing/noise_filter.py — Remove Non-Diagnostic Noise
----------------------------------------------------------------
PURPOSE:
    Strips content that adds no diagnostic value to the bug report.
    Keeps stack traces, error messages, and meaningful text intact.

WHAT IT REMOVES:
    - Memory address lines (0x82e00000-0x82e10000 rwxp ...)
    - /proc/ memory map entries
    - JAR file path listings (/home/.../plugins/...)
    - Hex dump blocks

CAPABILITIES (can be extended later):
    - Custom regex patterns via config
    - Whitelist patterns (never filter these)
    - Confidence scoring (how much noise was removed)
    - Language-specific filters (Java, Python, JS)

CONNECTS TO:
    preprocessing/__init__.py → runs after text_cleaner.clean()
"""

import re

NOISE_PATTERNS = [
    # 1. Memory address ranges & system maps (Universal)
    re.compile(
        r"^[0-9a-f]{8,16}-[0-9a-f]{8,16}\s+[\w-]{4}\s+[0-9a-f]+.*$",
        re.MULTILINE | re.IGNORECASE,
    ),
    # 2. Hex dumps / Standalone Hex addresses
    re.compile(r"^0x[0-9a-f]+\s*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^\s*(?:[0-9a-f]{2}\s+){8,}.*$", re.MULTILINE | re.IGNORECASE),
    # 3. Environment/System Path listings
    re.compile(
        r"^.*[/\\](?:lib|bin|plugins|node_modules|site-packages)[/\\][\w.\-]+\.(?:so|dll|jar|pyc|exe|dylib)\s*$",
        re.MULTILINE | re.IGNORECASE,
    ),
    # 4. Runtime Memory/Resource Summaries
    re.compile(
        r"^\s*(?:Heap|GC|Thread|Memory|Object|Handle|PSYoungGen|ParOldGen|total|used|eden|from|to)\s+(?:summary|total|count|info|stats|:)\s*.*$",
        re.MULTILINE | re.IGNORECASE,
    ),
    # 5. Low-level Thread/Register Dumps
    re.compile(
        r"^.*(?:prio=\d+|tid=0x|nid=0x|rax=|rbx=|rcx=|eip=|esp=).*$",
        re.MULTILINE | re.IGNORECASE,
    ),
    # 6. CSV/Log Padding
    re.compile(r"^[ \t\"']+$", re.MULTILINE),
]


def filter_noise(text: str) -> str:
    """Remove non-diagnostic noise lines from any technical log or report."""
    if not text:
        return ""

    for pattern in NOISE_PATTERNS:
        text = pattern.sub("", text)

    text = re.sub(r"^[=\-_*#]{5,}\s*$", "", text, flags=re.MULTILINE)

    return "\n".join([line for line in text.splitlines() if line.strip()])


if __name__ == "__main__":
    test_input = """
    82e00000-82e10000 rwxp 00000000 00:00 0
    Actual Error: NullPointerException
    0x00007ffd
    PSYoungGen total 59904K, used 2423K
    rax=0000000000000000 rbx=0000000000000000
    at app.main(main.go:15)
    """
    print("--- NOISE FILTER TEST ---")
    print(filter_noise(test_input))
