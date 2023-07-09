def split_string(string):
    # Removing the parentheses and splitting the string by comma
    parts = string[1:-2].split(",")
    # Removing the whitespace and quotes from the parts
    parts = [part.strip().strip("'") for part in parts]
    print(parts)
    return parts[0], ' '.join(parts[1:])


def return_iters(db: str  # Path to db
                 ):
    file = open(db, 'r', encoding='latin1')
    mapping = {
        "Libertarian Left": 0,
        "Libertarian Right": 1,
        "Authoritarian Left": 2,
        "Authoritarian Right": 3,
        "Centrist": 4,
        "Authoritarian Center": 5,
        "Left": 6,
        "Right": 7,
        "Libertarian Center": 8,
    }
    lines = file.readlines()
    train = open("_train.csv", 'a', encoding='latin1')
    test = open("_test.csv", 'a', encoding='latin1')
    train.write('text,label\n')
    test.write('text,label\n')
    i = 0
    for line in lines:
        opinion, text = split_string(line)
        if i < 19451:
            test.write(text + ',' + str(mapping[opinion]) + '\n')
        else:
            train.write(text + ',' + str(mapping[opinion]) + '\n')
        i = i + 1
    train.close()
    test.close()


return_iters('194511_DB_Hot_Top_New')
