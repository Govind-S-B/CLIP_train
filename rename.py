import os
import shutil
import glob

# Function to perform the renaming and copying
def rename_and_copy_files(starting_number):
    # Directories
    source_directory = "prefiltered_data"
    destination_directory = "renamed_data"
    
    # Ensure the destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # Get list of files from source directory
    files = glob.glob(os.path.join(source_directory, '*'))
    
    # Iterate and copy files
    current_number = starting_number
    for file_path in files:
        # Get file extension
        file_name, file_extension = os.path.splitext(file_path)
        
        # Create new file name
        new_file_name = f"{current_number}{file_extension}"
        new_file_path = os.path.join(destination_directory, new_file_name)
        
        # Copy the file
        shutil.copy(file_path, new_file_path)
        
        # Increment the number
        current_number += 1

def main():
    # Ask user for the starting number
    try:
        starting_number = int(input("Enter the starting number: "))
    except ValueError:
        print("Please enter a valid integer for starting number.")
        return
    
    # Perform the operation
    rename_and_copy_files(starting_number)
    print("Files have been renamed and copied successfully.")

if __name__ == "__main__":
    main()
