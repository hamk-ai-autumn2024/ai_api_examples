def read_docx(file_path):
    """
    Read a Word (.docx) file and return its text content as a string.
    
    Args:
        file_path (str): Path to the .docx file
        
    Returns:
        str or None: Text content of the file if successful, None otherwise
    """
    try:
        # Import the necessary module
        import docx
        
        # Check if file exists
        import os
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist")
            return None
        
        # Check file extension
        if not file_path.lower().endswith('.docx'):
            print(f"Error: File '{file_path}' is not a .docx file")
            return None
        
        # Open the document
        doc = docx.Document(file_path)
        
        # Extract text from paragraphs
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        
        # Join all paragraphs into a single string
        return '\n'.join(full_text)
    
    except ImportError:
        print("Error: 'python-docx' module not installed. Please install it using 'pip install python-docx'")
        return None
    except docx.opc.exceptions.PackageNotFoundError:
        print(f"Error: File '{file_path}' is not a valid .docx file or is corrupted")
        return None
    except PermissionError:
        print(f"Error: Permission denied when accessing '{file_path}'")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return None
    
# Test the function
def main():
    file_path = 'BashTutorial.docx'
    text = read_docx(file_path)
    if text:
        print(text)

if __name__ == '__main__':
    main()
    