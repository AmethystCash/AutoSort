import time
import inflect
p = inflect.engine()


def rn_fancy():
    day = int(time.strftime("%e"))
    nice_datetime = time.strftime(f"%X - %B {p.ordinal(day)} %Y")
    return nice_datetime
