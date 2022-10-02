# This is a sample Python script.
import elicitation
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ast import literal_eval as make_tuple

def createNewEqualDB():
    file1 = open("controversialOnlyMainCMD.txt", "r")
    # file2 = open("database.txt", "r")
    file3 = open("databaseTop.txt", "r")
    writeToFile = open("NewDB.txt", "w")
    c = [2000, 2000, 2000, 2000]
    mapping = {
        "Libertarian Left": 0,
        "Libertarian Right": 1,
        "Authoritarian Left": 2,
        "Authoritarian Right": 3,
    }
    for line in file1:
        opinion, text = make_tuple(line)
        index = mapping[opinion]
        if (c[index] > 0):
            c[index] -= 1
            writeToFile.write(line)
    print(c)
    # for line in file2:
    #     opinion, text = make_tuple(line)
    #     index = mapping[opinion]
    #     if (c[index] > 0):
    #         c[index] -= 1
    #         writeToFile.write(line)
    # print(c)
    for line in file3:
        opinion, text = make_tuple(line)
        index = mapping[opinion]
        if (c[index] > 0):
            c[index] -= 1
            writeToFile.write(line)
    print(c)

def main():
    createNewEqualDB()
    # rn = elicitation.Elicitation()
    # rn.run()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
