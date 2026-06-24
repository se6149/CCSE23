# -*- coding: utf-8 -*-
import re
from pathlib import Path

IN_FILE = r"J:\开发区\测图1\AA留痕工具\古诗词.txt"
OUT_FILE = r"J:\开发区\测图1\AA留痕工具\输出.txt"


def read_text(path):
    data = Path(path).read_bytes()
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb2312"):
        try:
            return data.decode(enc)
        except Exception:
            pass
    return data.decode("utf-8", errors="ignore")


def extract_poems(text):
    results = []

    # 每个 result-item 当作一首诗
    blocks = re.findall(
        r'<div[^>]*class="result-item"[^>]*>(.*?)</div>\s*</div>',
        text,
        flags=re.S
    )

    for block in blocks:
        # ---------- 标题 ----------
        title_match = re.search(
            r'class="name">\s*([^<]+)\s*<',
            block
        )
        title = title_match.group(1).strip() if title_match else ""

        # ---------- 作者（去掉朝代） ----------
        author_match = re.search(
            r'[\u4e00-\u9fa5]+·\s*([\u4e00-\u9fa5]{2,4})',
            block
        )
        author = author_match.group(1).strip() if author_match else ""

        # ---------- 诗文 ----------
        lines = re.findall(
            r'class="poem-line-item">\s*([^<]+)\s*<',
            block
        )
        poem = "".join(line.strip() for line in lines)

        # ---------- 严格校验 ----------
        if title and author and poem:
            results.append(f"{title}----{author}----{poem}")

    return results


def main():
    text = read_text(IN_FILE)
    poems = extract_poems(text)

    Path(OUT_FILE).write_text(
        "\n".join(poems),
        encoding="utf-8"
    )

    print(f"✔ 成功写入 {len(poems)} 首诗到：{OUT_FILE}")


if __name__ == "__main__":
    main()
