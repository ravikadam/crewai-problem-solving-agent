import os
from datetime import datetime


def save_document_to_file(content: str, filename: str, file_format: str = "md") -> str:
    """
    Save document content to a local file with timestamp.
    
    Args:
        content: The content to write to the file
        filename: The base filename (without extension)
        file_format: File format/extension (md, txt, etc.)
    
    Returns:
        Success message with file path or error message
    """
    try:
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create full filename with timestamp
        full_filename = f"{timestamp}_{filename}.{file_format}"
        filepath = os.path.join(output_dir, full_filename)
        
        # Write content to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"File successfully saved to: {filepath}"
        
    except Exception as e:
        return f"Error saving file: {str(e)}"
