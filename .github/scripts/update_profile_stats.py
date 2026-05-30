#!/usr/bin/env python3
import json
import re
import sys
import urllib.request

USERNAME = "zhk0567"
README_PATH = "README.md"


def fetch_stats():
    with urllib.request.urlopen(f"https://api.github.com/users/{USERNAME}") as resp:
        data = json.load(resp)
    return data["public_repos"], data["followers"], data["following"]


def build_header_badge(repos: int) -> str:
    return (
        f"[![Repos](https://img.shields.io/badge/"
        f"公开仓库-{repos}-36BCF7?style=for-the-badge&logo=github&logoColor=white)]"
        f"(https://github.com/{USERNAME}?tab=repositories)"
    )


def build_github_section(repos: int) -> str:
    return "\n".join(
        [
            f"[![Followers](https://img.shields.io/github/followers/{USERNAME}?label=Followers&style=flat-square&logo=github&logoColor=white&color=36BCF7)](https://github.com/{USERNAME}?tab=followers)",
            f"[![Following](https://img.shields.io/github/following/{USERNAME}?label=Following&style=flat-square&logo=github&logoColor=white&color=6C63FF)](https://github.com/{USERNAME}?tab=following)",
            f"[![Repos](https://img.shields.io/badge/Repos-{repos}-36BCF7?style=flat-square&logo=github&logoColor=white)](https://github.com/{USERNAME}?tab=repositories)",
            f"[![Algorithm](https://img.shields.io/badge/活跃仓库-Algorithm-6C63FF?style=flat-square&logo=github&logoColor=white)](https://github.com/{USERNAME}/Algorithm)",
        ]
    )


def replace_block(content: str, marker: str, replacement: str) -> str:
    pattern = rf"<!-- {marker} -->.*?<!-- /{marker} -->"
    block = f"<!-- {marker} -->\n{replacement}\n<!-- /{marker} -->"
    return re.sub(pattern, block, content, count=1, flags=re.DOTALL)


def main() -> int:
    repos, followers, following = fetch_stats()
    print(f"public_repos={repos}, followers={followers}, following={following}")

    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()

    updated = replace_block(content, "profile:header-repos", build_header_badge(repos))
    updated = replace_block(updated, "profile:github-stats", build_github_section(repos))

    if updated == content:
        print("README stats already up to date.")
        return 0

    with open(README_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(updated)

    print("README stats updated.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
