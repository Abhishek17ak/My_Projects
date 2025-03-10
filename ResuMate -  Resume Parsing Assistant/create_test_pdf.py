from fpdf import FPDF
import textwrap

def create_resume_pdf(input_txt, output_pdf):
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=12)
    
    # Read text file
    with open(input_txt, 'r', encoding='utf-8') as file:
        text = file.readlines()
    
    # Add content to PDF
    y_position = 10
    for line in text:
        # Handle empty lines
        if line.strip() == "":
            y_position += 5
            continue
        
        # Check if line is a header (all caps)
        if line.strip().isupper():
            pdf.set_font("Arial", 'B', 14)
            pdf.set_xy(10, y_position)
            pdf.cell(0, 5, line.strip(), ln=True)
            y_position += 8
            pdf.set_font("Arial", size=12)
        else:
            # Wrap text to fit page width
            wrapped_lines = textwrap.wrap(line.strip(), width=95)
            for wrapped_line in wrapped_lines:
                pdf.set_xy(10, y_position)
                pdf.cell(0, 5, wrapped_line, ln=True)
                y_position += 6
    
    # Save PDF
    pdf.output(output_pdf)

if __name__ == "__main__":
    create_resume_pdf("test_resume.txt", "test_resume.pdf") 