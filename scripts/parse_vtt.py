#!/usr/bin/env python3
"""VTT 자막 파일에서 깨끗한 텍스트를 추출하는 스크립트 (macOS / Linux, Python3)
사용법: python3 parse_vtt.py sermon.ko.vtt
"""
import re
import sys

def main():
    vtt_path = sys.argv[1]
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # WEBVTT 헤더 및 메타데이터 블록 제거
    content = re.sub(r"WEBVTT\r?\n.*?\r?\n\r?\n", "", content, flags=re.S)
    content = re.sub(r"Kind:.*?\r?\n", "", content)
    content = re.sub(r"Language:.*?\r?\n", "", content)

    # 타임코드 라인 제거 (예: 00:00:01.000 --> 00:00:04.000)
    content = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}[^\r\n]*\r?\n", "", content)

    # 인라인 타이밍 태그 제거 (예: <00:00:01.000>)
    content = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", "", content)

    # <c>, </c>, <i>, </i> 등 HTML 태그 제거
    content = re.sub(r"<[^>]+>", "", content)

    # 빈 cue 번호 줄 제거 (숫자만 있는 줄)
    content = re.sub(r"(?m)^\d+\s*$", "", content)

    lines = [line.strip() for line in re.split(r"\r?\n", content) if line.strip() != ""]

    # 중복 연속 줄 제거 (YouTube VTT 오버랩 특성)
    result = []
    for line in lines:
        if result and result[-1] == line:
            continue
        result.append(line)

    output = " ".join(result)
    output = re.sub(r"\s{2,}", " ", output).strip()
    print(output)

if __name__ == "__main__":
    main()
