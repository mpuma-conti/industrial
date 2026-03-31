import pylnk3

with open("python\Lkn_binary\Ennovation Inkabor.lnk", "rb") as f:
    lnk = pylnk3.parse(f)

print(lnk)