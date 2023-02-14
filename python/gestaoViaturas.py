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
            print(f"'{licensePlate}' - License Plate inválid")
        # else:
            # print(f"'{licensePlate}' - License Plate válid")
        # if not brand:
        #   raise InvalidVehicleAttribute(f"")

        self.licensePlate = licensePlate
        self.brand = brand
        self.model = model
        self.date = date


class InvalidVehicleAttribute(ValueError):
    pass


def main() -> None:
    vehicle1 = Vehicle("10-XY-20", "Opel", "Corsa XL", 2019-10-15)


if __name__ == '__main__':
    main()
