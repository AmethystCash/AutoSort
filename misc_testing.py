import time
import inflect
p = inflect.engine()

print(time.strftime("%X %x"))
print(time.strftime("%x %X"))

# text=f"""Server creation date: {creation_time.strftime(f'{p.ordinal(creation_time.strftime("%d"))} %B %Y')}""")


def rn_fancy():
    day = int(time.strftime("%e"))
    nice_datetime = time.strftime(f"%X - %B {p.ordinal(day)} %Y")
    return nice_datetime

print(rn_fancy())