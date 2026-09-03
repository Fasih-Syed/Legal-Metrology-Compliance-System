from compliance.format_rules import validate_unit_sale_price


result = validate_unit_sale_price(
    net_quantity="100 g",
    mrp="125.00",
    declared_unit_price={
        "price": "1.25",
        "unit": "g"
    }
)


print("\n========== UNIT SALE PRICE ==========\n")

print("Status:", result["status"])
print("Declared:", result["declared"])
print("Expected:", result["expected"])
print("Message:", result["message"])