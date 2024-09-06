# text = "link to hk resources"
# yes = False

# for each in text.split(" "):
#     if each in ["hk", "resources"]:
#         yes = True
#         continue

#     print(each, "not in", ["hk", "resources"])

# print(yes)

import os
os.chdir("../animals-classifier")
print(os.getcwd())
dir_content = os.listdir()

for each_content in dir_content:
    if os.path.isdir(each_content):
        print(f"[DIR/] {each_content}/")
    else:
        print(f"[FILE] {each_content}")