def search_file(file):
    print 'Searching file %s' % (file)
    my_file = open(file,'r')
    file_content = my_file.read()
    my_file.close()
    while True:
        search_text = (yield)                             #Compulsory
        search_result = file_content.count(search_text)
        print 'Number of matches: %d' % (search_result)

a = search_file("POSCAR")
a.next()
a.send('Direct')                               # to search 'Direct' in file
