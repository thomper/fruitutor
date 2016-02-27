LETTERS = 'th'

def best_total(words, letters):
    'Return words sorted by most occurences of letters.'
    return sorted(words, key=lambda word: -sum((word.count(l) for l in letters)))

def best_ratio(words, letters):
    'Return words sorted by the highest proportion of characters in letters.'
    return sorted(words, key=lambda word: -sum((word.count(l) / len(word) for l in letters)))

def get_input():
    lines = []
    try:
        while True:
            lines.append(input().strip())
    except EOFError:
        pass
    words = []
    for line in lines:
        words.extend(words_from_line(line))
    return tuple((word for word in words if len(word) >= 1))

def words_from_line(line):
    return tuple((word.strip().lower() for word in line.split(',')))

def main():
    words = get_input()
    for word in best_ratio(words, LETTERS):
        print(word)

if __name__ == '__main__':
    main()
