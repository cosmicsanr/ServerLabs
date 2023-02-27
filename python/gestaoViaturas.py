from datetime import date
import re


CSV_DEFAULT_DELIM = ','
DEFAULT_INDENTATION = 3


class Vehicle:
    def __init__(self,
                 licensePlate: str,
                 brand: str,
                 model: str,
                 date: date,
                 ):

        regexLicense = re.compile(
            r"^(\d{2}\-[A-Z]{2}\-\d{2})|([A-Z]{2}\-\d{2}\-[A-Z]{2})")
        if not re.fullmatch(regexLicense, licensePlate):
            print(f"'{licensePlate}' - License Plate invalid")
        else:
            print(f"'{licensePlate}' - License Plate válid")

        regexBrand = re.compile(
            r"^[A-Z].{3,}$")
        if not re.fullmatch(regexBrand, brand):
            print(f"{brand}' - Brand invalid")
        else:
            print(f"'{brand}' - brand valid")

        regexModel = re.compile(
            r"(^[0-9].{3,}$)|(^[A-Z].{3,}$)")
        if not re.fullmatch(regexModel, model):
            print(f"'{model}' - Model invalid")
        else:
            print(f"'{model}' - Model valid")

        regexDate = re.compile(
            r"^((1[9]\d{2})|(20[0-3]\d))\-((0[1-9])|(1[0-2]))\-((0[1-9])|(1\d)|(2\d)|(3[0-1](?!\/02)))$")
        if not re.fullmatch(regexDate, date):
            print(f"'{date}' - Date not valid")
        else:
            print(f"'{date}' - Date valid")

        self.licensePlate = licensePlate
        self.brand = brand
        self.model = model
        self.date = date


def __str__(self) -> str:
    cls_name = self.__class__.__name__


def main() -> None:
    vehicle1 = Vehicle("10-XY-20", "Opel", "Corsa XL", "2019-10-15")


if __name__ == '__main__':
    main()
