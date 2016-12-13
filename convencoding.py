def conv(filename):
    target_file = "exportCPfix.csv"
    with open(filename, 'rb') as source_file:
        with open(target_file, 'w+b') as dest_file:
            contents = source_file.read()
            dest_file.write(contents.decode('utf-16').encode('utf-8'))
            return target_file;
