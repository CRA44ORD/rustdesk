"""StateZero branding patch - exact line replacement, no regex.

Replaces whole lines by prefix match, so upstream value changes can't
cause partial-line corruption (as sed did). Fails loudly on mismatch.
Run from repo root:  python3 brand_patch.py
"""
import sys

CONFIG = "libs/hbb_common/src/config.rs"
SERVER_LINE = 'pub const RENDEZVOUS_SERVERS: &[&str] = &["rds.statezero.co"];'
KEY_LINE = 'pub const RS_PUB_KEY: &str = "mbq7tvEAOL0Jn8+Jrl8ytQhIVod6IgfGwZdY7ut8oqw=";'


def main() -> int:
    with open(CONFIG, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    hits = {"srv": 0, "key": 0, "app": 0}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("pub const RENDEZVOUS_SERVERS:"):
            lines[i] = SERVER_LINE
            hits["srv"] += 1
        elif stripped.startswith("pub const RS_PUB_KEY:"):
            lines[i] = KEY_LINE
            hits["key"] += 1
        elif stripped.startswith("pub static ref APP_NAME:"):
            if '"RustDesk"' not in line:
                print(f"APP_NAME line already branded: {line.strip()}")
                hits["app"] += 1
            else:
                lines[i] = line.replace('"RustDesk"', '"StateZeroRDS"')
                hits["app"] += 1
    if hits != {"srv": 1, "key": 1, "app": 1}:
        print(f"BRANDING MISS: {hits}", file=sys.stderr)
        return 1
    with open(CONFIG, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"branding ok: {hits}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
