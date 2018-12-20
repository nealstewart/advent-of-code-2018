
def get_counts(id: str):
    counts = dict()
    for char in id:
        if char not in counts:
            counts[char] = 1
        else:
            counts[char] += 1

    return counts


double_count = 0
triple_count = 0

with open('input.csv') as f:
    for line in f:
        stripped = line.strip()
        counts = get_counts(stripped)
        if any(count == 2 for count in counts.values()):
            double_count += 1 
        if any(count == 3 for count in counts.values()):
            triple_count += 1 

print(double_count)
print(triple_count)
print(double_count * triple_count)