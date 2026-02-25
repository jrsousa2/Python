# from pathlib import Path
import re

time_shift = 3.8  # seconds to shift (can be negative)
input_file = r"D:\Downloads_Torrents_Complete\Annie Hall (1977)\Annie.Hall.1977.720p.HDTV.x264.YIFY.srt"
output_file = r"D:\Downloads_Torrents_Complete\Annie Hall (1977) [1080p]\Annie.Hall.1977.1080p.BluRay.x264.YIFY.srt"
# dst_folder.mkdir(exist_ok=True)

time_pattern = re.compile(r"(\d+):(\d+):(\d+),(\d+)")

def shift_time(h, m, s, ms, shift):
    total = int(h)*3600 + int(m)*60 + int(s) + float(ms)/1000 + shift
    if total < 0: total = 0
    h_new = int(total // 3600)
    m_new = int((total % 3600) // 60)
    s_new = int(total % 60)
    ms_new = int(round((total - int(total)) * 1000))
    return f"{h_new:02}:{m_new:02}:{s_new:02},{ms_new:03}"

with open(input_file, encoding="utf-8") as f:
    lines = []
    for line in f:
        if "-->" in line:
            start, end = line.split(" --> ")
            start = shift_time(*map(int, re.split(r"[:,]", start)), time_shift)
            end = shift_time(*map(int, re.split(r"[:,]", end)), time_shift)
            line = f"{start} --> {end}\n"
        lines.append(line)
    # (dst_folder/file.name).write_text("\n".join(lines), encoding="utf-8")

with open(output_file, "w", encoding="utf-8") as f:
     f.writelines(lines)