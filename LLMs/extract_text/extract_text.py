import PyPDF2
import argparse
import os
import re

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            extracted_text = ""
            previous_page_text = ""

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()

                # Remove repetitive headers and footers by comparing to previous page
                if page_text.startswith(previous_page_text[:100]):
                    page_text = page_text[len(previous_page_text[:100]):]
                previous_page_text = page_text

                extracted_text += page_text.strip() + "\n\n"  # Add double newlines for paragraph separation

            return extracted_text
    except Exception as e:
        print(f"Error: {e}")
        return None

def identify_headings(text):
    # Regular expression to identify potential headings
    headings_pattern = re.compile(r'\b[A-Z][A-Z\s&,-]+\b')
    headings = set(match.group().strip() for match in headings_pattern.finditer(text))
    return headings

def clean_text(text, headings):
    # Remove unnecessary spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)  # Remove spaces before punctuation
    text = text.replace(" \n", "\n").replace("\n ", "\n")  # Remove spaces around newlines

    # Handle hyphenated words at the end of lines
    text = re.sub(r'-\n', '', text)  # Join hyphenated words
    text = re.sub(r'\n', ' ', text)  # Replace newlines with spaces
    text = re.sub(r' {2,}', ' ', text)  # Replace multiple spaces with a single space

    # Normalize paragraph formatting
    paragraphs = text.split('. ')
    paragraphs = [p.strip().capitalize() + '.' for p in paragraphs if p]
    cleaned_text = '\n\n'.join(paragraphs)

    # Apply custom formatting rules conditionally
    # Format detected headings
    for heading in headings:
        cleaned_text = re.sub(r'\b' + re.escape(heading) + r'\b', f'### {heading} ###', cleaned_text, flags=re.IGNORECASE)

    # Detect and format bullet points
    if re.search(r'\s-\s', text):
        cleaned_text = re.sub(r'\s-\s', r'\n- ', cleaned_text)

    # Detect and format tables
    if re.search(r'\|\s+\|', text):
        cleaned_text = re.sub(r'\|\s+', '|', cleaned_text)  # Remove spaces after vertical bars
        cleaned_text = re.sub(r'\s+\|', '|', cleaned_text)  # Remove spaces before vertical bars
        cleaned_text = re.sub(r'\|\s+\|\s+', '|', cleaned_text)  # Remove spaces between columns

    # Ensure consistent spacing around newlines
    cleaned_text = cleaned_text.replace('\n ', '\n').replace(' \n', '\n')

    return cleaned_text

def save_text_to_file(text, file_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract text from a PDF and save it to a text file.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("output_directory", help="Directory to save the extracted text file")

    # Parse arguments
    args = parser.parse_args()

    # Extract text from PDF
    text = extract_text_from_pdf(args.pdf_path)
    
    if text:
        # Identify headings
        headings = identify_headings(text)

        # Clean the extracted text
        cleaned_text = clean_text(text, headings)

        # Create output file name
        pdf_filename = os.path.basename(args.pdf_path)
        output_filename = os.path.splitext(pdf_filename)[0] + ".txt"
        output_file_path = os.path.join(args.output_directory, output_filename)
        
        # Save to a text file
        save_text_to_file(cleaned_text, output_file_path)
    else:
        print("No text extracted or an error occurred.")
