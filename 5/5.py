def are_combineable(a: str, b: str) -> bool:
    return a.lower() == b.lower() and a != b

def combine_all(target: str) -> str:
    while True:
        combined = ['']
        for char in target:
            if are_combineable(combined[-1], char):
                del combined[-1]
            else:
                combined.append(char)

        new_string = ''.join(combined)
        if len(new_string) == len(target):
            return target

        target = new_string

def get_input():
    with open('input', 'r') as myfile:
        return myfile.read().replace('\n', '')

def combine_with_one_removed(target: str, type: str) -> str:
    while True:
        combined = ['']
        for char in target:
            if (char.lower() == type.lower()):
                continue
            elif are_combineable(combined[-1], char):
                del combined[-1]
            else:
                combined.append(char)

        new_string = ''.join(combined)
        if len(new_string) == len(target):
            return target

        target = new_string

formula = get_input()
print("Exercise 1", len(combine_all(formula)))

letters = [chr(num) for num in range(97, 123)]
smallest = min([(letter, len(combine_with_one_removed(formula, letter))) for letter in letters], key=lambda t: t[1])
print("exercise 2", smallest)

