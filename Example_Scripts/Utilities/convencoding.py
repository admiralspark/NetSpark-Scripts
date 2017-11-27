'''
-------------------------------------------------------------------------------
This function simply converts a file to UTF-8 from UTF-16. It's needed for
Solarwinds integration
-------------------------------------------------------------------------------
'''

def conv(filename):
    """Takes a file name string as input, converts to UTF-8"""
    target_file = input('What is the name of the customer? \n') + ".csv"
    with open(filename, 'rb') as source_file:
        with open(target_file, 'w+b') as dest_file:
            contents = source_file.read()
            dest_file.write(contents.decode('utf-16').encode('utf-8'))
            return target_file
