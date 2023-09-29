data = 'mississippi'
counter = {}

for letter in data:
    counter[letter] = counter.get(letter, 0) + 1

print(counter)
