"""
Covert column number into excel column
127 => AA
"""

def convert_to_excel_col(n):
    n = n-1
    alpha_dict = dict()
    result_list = []
    for i, val in enumerate(range(ord('A'), ord('Z')+1)):
        alpha_dict[i] = chr(val)

    print alpha_dict
    while(n>=26):
        result_list.append(alpha_dict[(n % 26)])
        n = n/26
    else:
        result_list.append(alpha_dict[n-1])
    result_list.reverse()
    print result_list, 

def main():
    convert_to_excel_col(28)

if __name__ == "__main__":
    main()