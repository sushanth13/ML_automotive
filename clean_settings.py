import os, glob

pages_dir = r"c:\Users\jana.sushanth.EXAFLUENCE-INC\Downloads\Santa-uptd (2)\Santa-uptd\Santa\pages"
html_files = glob.glob(os.path.join(pages_dir, "*.html"))

for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if 'href="/settings"' not in line:
            new_lines.append(line)
            
    with open(fpath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

# Delete settings files
s1 = os.path.join(pages_dir, "settings.html")
s2 = r"c:\Users\jana.sushanth.EXAFLUENCE-INC\Downloads\Santa-uptd (2)\Santa-uptd\Santa\templates\pages\settings.html"
if os.path.exists(s1): os.remove(s1)
if os.path.exists(s2): os.remove(s2)
