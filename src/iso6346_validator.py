def char_to_num(c):
    if c.isdigit():
        return int(c)
    val = ord(c.upper()) - ord('A') + 10
    if val >= 11: val += 1
    if val >= 22: val += 1
    if val >= 33: val += 1
    return val

def iso6346_check_digit(serial10):
    if len(serial10) != 10:
        return '0'
    total = 0
    powers = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    for i, char in enumerate(serial10):
        total += char_to_num(char) * powers[i]
    remainder = total % 11
    return '0' if remainder == 10 else str(remainder)

def validate_container(full_code):
    if len(full_code) != 11:
        return False, 'Invalid length'
    serial10 = full_code[:10].upper()
    actual = full_code[10]
    expected = iso6346_check_digit(serial10)
    return actual == expected, expected

print("🚢 ISO 6346 VALIDATOR (NO ERRORS):")
test_codes = ['CSQU3054383']
for code in test_codes:
    valid, expected = validate_container(code)
    status = "✅ VALID" if valid else "❌ INVALID"
    print(f"  {code}: {status} (check: {expected})")

print("\n🚢 GENERATED VALID CODES:")
for i in range(3):
    serial10 = f"CSQU305438{i}"
    check = iso6346_check_digit(serial10)
    full_code = serial10 + check
    print(f"  {full_code} ✅ (check: {check})")
