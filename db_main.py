# This is a sample Python script.
import elicitation
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ast import literal_eval as make_tuple

def merageAllDBToOne():
    file_1 = open("controversialOnlyMainCMD.txt", "r")
    file_2 = open("databaseTop.txt", "r")
    file_3 = open("controversial.txt", "r")
    file_4 = open("DB", "r")
    file_5 = open("NewDB.txt", "r")
    file_6 = open("NewPostDB.txt", "r")
    newDBFile = open("uniqueDB.txt","a")
    newDBlst = []
    files = [file_1,file_2,file_3,file_4,file_5,file_6]
    for file in files:
        for line in file:
            if line not in newDBlst:
                newDBlst.append(line)
    for row in newDBlst:
        newDBFile.write(row)
    print("DONE")


def countEachRole():
    uniqueDB = open("uniqueDB.txt", "r")
    unique_role_count = {
        "Libertarian Left": 0,
        "Libertarian Right": 0,
        "Authoritarian Left": 0,
        "Authoritarian Right": 0,
    }
    for line in uniqueDB:
        opinion, text = make_tuple(line)
        unique_role_count[opinion] += 1
    print(unique_role_count)


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
    # countEachRole()
    # createNewEqualDB()
    rn_Hot = elicitation.Elicitation()
    rn_Hot.run("hot")

    rn_New = elicitation.Elicitation()
    rn_New.run("new")

    rn_Top = elicitation.Elicitation()
    rn_Top.run("top")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
