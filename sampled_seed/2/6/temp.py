def readf():
    fh_read = open(my_file, errors='replace')
    for line in fh_read:
        print(line)
readf()