from algorithm import engine, read_file, txt_to_matrix

if __name__ == '__main__':
    fixed_operation = txt_to_matrix('fixed_operations.txt')
    print(f"Fixed operations: {fixed_operation}")