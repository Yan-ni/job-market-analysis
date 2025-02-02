import os

def get_filenames(path):
    """Retrieve sorted list of filenames in the given directory."""
    return sorted(os.listdir(path))

def read_file(file_path):
    """Read the content of a file and return it as a string."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_test_data(test_data_dir_path):
    """Load test data by matching files between input and expected directories."""
    input_dir = os.path.join(test_data_dir_path, 'input')
    expected_dir = os.path.join(test_data_dir_path, 'expected')

    input_filenames = get_filenames(input_dir)
    expected_filenames = get_filenames(expected_dir)
    
    assert input_filenames == expected_filenames, \
        f"Mismatch between input and expected files: {input_filenames} vs {expected_filenames}"

    test_data = []
    for filename in input_filenames:
        input_file_path = os.path.join(input_dir, filename)
        expected_file_path = os.path.join(expected_dir, filename)
        
        input_content = read_file(input_file_path)
        expected_content = read_file(expected_file_path)
        
        test_data.append((input_content, expected_content, filename.split('.')[0]))
    return test_data



