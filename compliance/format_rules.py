import re


def parse_quantity(quantity):
    """
    Converts a quantity such as '100 g' into
    a numeric value and normalized unit.
    """

    if not quantity:
        return None, None

    match = re.search(
        r"([\d.]+)\s*(mg|g|kg|ml|l)",
        quantity,
        re.IGNORECASE
    )

    if not match:
        return None, None

    value = float(match.group(1))
    unit = match.group(2).lower()

    return value, unit


def calculate_expected_unit_price(net_quantity, mrp):
    """
    Calculates the expected unit sale price.

    Weight-based commodities:
    - Below 1 kg -> per gram
    - 1 kg or more -> per kilogram
    """

    quantity, unit = parse_quantity(net_quantity)

    if quantity is None or mrp is None:
        return None

    mrp_value = float(mrp)

    if unit == "kg":
        quantity_in_grams = quantity * 1000

    elif unit == "g":
        quantity_in_grams = quantity

    elif unit == "mg":
        quantity_in_grams = quantity / 1000

    else:
        return None

    if quantity_in_grams <= 0:
        return None

    if quantity_in_grams < 1000:
        expected = mrp_value / quantity_in_grams

        return {
            "value": round(expected, 2),
            "unit": "g"
        }

    else:
        quantity_in_kg = quantity_in_grams / 1000
        expected = mrp_value / quantity_in_kg

        return {
            "value": round(expected, 2),
            "unit": "kg"
        }


def validate_unit_sale_price(
    net_quantity,
    mrp,
    declared_unit_price
):
    """
    Compares the declared unit sale price against
    the calculated expected value.
    """

    if not declared_unit_price:
        return {
            "status": "NOT_FOUND",
            "declared": None,
            "expected": None,
            "message": "Unit sale price was not detected."
        }

    expected = calculate_expected_unit_price(
        net_quantity,
        mrp
    )

    if expected is None:
        return {
            "status": "UNABLE_TO_VALIDATE",
            "declared": declared_unit_price,
            "expected": None,
            "message": (
                "Unable to calculate the expected unit sale price."
            )
        }

    declared_value = float(
        declared_unit_price["price"].replace(",", "")
    )

    declared_unit = declared_unit_price["unit"].lower()

    if (
        round(declared_value, 2) == expected["value"]
        and declared_unit == expected["unit"]
    ):
        return {
            "status": "VALID",
            "declared": declared_unit_price,
            "expected": expected,
            "message": (
                f"Declared unit sale price matches the "
                f"calculated value: ₹{expected['value']}/{expected['unit']}."
            )
        }

    return {
        "status": "POTENTIAL_NON_COMPLIANCE",
        "declared": declared_unit_price,
        "expected": expected,
        "message": (
            f"Declared unit sale price does not match the "
            f"calculated value. Expected "
            f"₹{expected['value']}/{expected['unit']}."
        )
    }