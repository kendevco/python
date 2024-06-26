import sys
import re

def remove_tags(text):
    """
    Remove vtt markup tags
    """
    tags = [
        r'</c>',
        r'<c(\.color\w+)?>',
        r'<\d{2}:\d{2}:\d{2}\.\d{3}>',
        r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}',  # remove timestamps
    ]

    for pat in tags:
        text = re.sub(pat, '', text)

    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text


def remove_header(lines):
    """
    Remove vtt file header
    """
    pos = -1
    for mark in ('##', 'Language: en',):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos+1:]
    return lines

def merge_duplicates(lines):
    """
    Remove duplicated subtitles. Duplacates are always adjacent.
    """
    last_cap = ''
    for line in lines:
        if line == "" or re.match('^\d{2}:\d{2}$', line):
            continue
        if line != last_cap:
            yield line
            last_cap = line

def merge_short_lines(lines):
    buffer = ''
    for line in lines:
        if line == "" or re.match('^\d{2}:\d{2}$', line):
            yield '\n' + line
            continue

        if len(line+buffer) < 80:
            buffer += ' ' + line
        else:
            yield buffer.strip()
            buffer = line
    yield buffer

def main():
    # vtt_file_name = sys.argv[1]
    vtt_file_name = "C:\Data\Dev\Python\Input\BJCNetUpgradeRegroup_2023-06-30.vtt"
    txt_name =  re.sub(r'.vtt$', '.txt', vtt_file_name)
    with open(vtt_file_name) as f:
        text = f.read()
    text = remove_tags(text)
    lines = text.splitlines()
    lines = remove_header(lines)
    lines = merge_duplicates(lines)
    lines = list(lines)
    lines = merge_short_lines(lines)
    lines = list(lines)

    with open(txt_name, 'w') as f:
        for line in lines:
            f.write(line)
            f.write("\n")

if __name__ == "__main__":
    main()
