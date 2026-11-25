# THIS CODE SEARCHES FOR KEYWORDS IN MY .NB FILES
# CREATED THIS SINCE THERE ARE TOO MANY FILES 
# AND IT'S IMPOSSIBLE TO REMEMBER THE LOCATIONS
from pathlib import Path
import re

# SEARCH PATH
# search_path = Path(r"D:\Math\13o Paper-Flint")
search_path = Path(r"D:\Math\12o Paper-Functional")

pattern = '''Cell[BoxData[
 RowBox[{"Log", "[", 
  RowBox[{"Sin", "[", 
   RowBox[{"\\[Pi]", " ", "x"}], "]"}],'''

pattern = r'''
RowBox[{"PolyLog", "[",
RowBox[{"1", ",",
SuperscriptBox["\[ExponentialE]", "z"]
'''

# REMOVE ALL WHITESPACE (spaces, tabs, and line breaks) FROM SEARCH STRING
pattern = re.sub(r'\s+', '', pattern)

for file in search_path.rglob("*.nb"):
    try:
        text = file.read_text(encoding="utf-8", errors="ignore")

        # REMOVE ALL WHITESPACE FROM FILE CONTENT IN MEMORY
        text = re.sub(r'\s+', '', text)

        if pattern in text:
            print(file)

    except OSError:
        pass