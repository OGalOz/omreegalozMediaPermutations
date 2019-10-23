



def convert_list_to_tab_separated_string(inp_list_d1):
    output_str = ''
    for item in inp_list_d1:
        output_str += str(item) + '\t'
    output_str = output_str[:-1] + '\n'
    return output_str

def convert_d2_list_to_tab_separated_string(inp_list_d2):
    output_str = ''
    for list_d1 in inp_list_d2:
        output_str += convert_list_to_tab_separated_string(list_d1)
    return output_str[:-1]

def string_to_file(output_str,filename):
    f = open(filename,'w')
    f.write(output_str)
    f.close()


def import_media_tsv_to_cmpnd_list_d2(filename):

    
    
    
    #We assume the first row is the column headers:
    return 0


def test():
    test_list_d1 = ['a', 'b', 1, 2]
    test_list_d2 = [test_list_d1.copy() for i in range(4)]
    print(convert_d2_list_to_tab_separated_string(test_list_d2))

def main():
    test()

#main()
