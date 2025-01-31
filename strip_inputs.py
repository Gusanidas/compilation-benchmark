import os

def process_file(file_path):
    """
    Process a single input.txt file by stripping whitespace and removing leading/trailing blank lines.
    """
    try:
        # Read the file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Strip whitespace from each line
        lines = [line.strip() for line in lines]
        
        # Remove leading blank lines
        while lines and not lines[0]:
            lines.pop(0)
            
        # Remove trailing blank lines
        while lines and not lines[-1]:
            lines.pop()
            
        # Write back to the file
        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))
            if lines:  # Add final newline if file is not empty
                f.write('\n')
                
        print(f"Successfully processed: {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def find_and_process_input_files(root_dir):
    """
    Recursively search for input.txt files and process them.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'input.txt' in filenames:
            file_path = os.path.join(dirpath, 'input.txt')
            process_file(file_path)

# Usage
root_directory = "problems/misc_problems"
find_and_process_input_files(root_directory)