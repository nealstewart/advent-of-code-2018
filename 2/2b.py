

def get_lines():
    with open('input.csv') as f:
        return [f.strip() for f in f.readlines()]

def find_same():
    lines = get_lines()
    id_length = len(lines[0])
    for col in range(0, id_length):
        reduced_lines = [line[0:col] + line[col + 1:id_length] for line in lines]
        prev_lines = set()
        for line in reduced_lines:
            if (line in prev_lines):
                return line
            prev_lines.add(line)
        
    return None

print(find_same())