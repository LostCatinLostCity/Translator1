import streamlit as st
from googletrans import Translator
from PyPDF2 import PdfFileReader
from docx import Document as DocxDocument

# Initialize the translator
translator = Translator()

# Streamlit app
def main():
    st.title("English to Hindi Translator")

    # Sidebar choice
    choice = st.sidebar.selectbox("Select your choice", ["Translate Text", "Translate Document"])

    print(f"Choice: {choice}")

    if choice == "Translate Text":
        st.subheader("Translate Text")
        # Get user input for text
        input_text = st.text_area("Enter text in English:")
        if st.button("Translate") and input_text:
            try:
                # Translate text
                translated_text = translator.translate(input_text, src='en', dest='hi').text

                # Display the translation
                st.subheader("Translated text in Hindi:")
                st.write(translated_text)
            except Exception as e:
                st.error(f"Translation Error: {e}")

    elif choice == "Translate Document":
        st.subheader("Translate Document")
        # Get user input for document
        input_file = st.file_uploader("Upload your document here", type=['pdf', 'docx'])
        if input_file is not None:
            if st.button("Translate Document"):
                # Save the uploaded file
                with open("uploaded_file", "wb") as f:
                    f.write(input_file.getbuffer())

                # Translate based on file type
                if input_file.type == 'application/pdf':
                    text = extract_text_from_pdf("uploaded_file")
                elif input_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    text = extract_text_from_docx("uploaded_file")

                try:
                    # Translate text
                    translated_text = translator.translate(text, src='en', dest='hi').text

                    # Display the translation
                    st.subheader("Translated text in Hindi:")
                    st.write(translated_text)
                except Exception as e:
                    st.error(f"Translation Error: {e}")

def extract_text_from_pdf(file_path):
    # Extract text from a PDF file
    with open(file_path, "rb") as file:
        pdf_reader = PdfFileReader(file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

def extract_text_from_docx(file_path):
    # Extract text from a DOCX file
    doc = DocxDocument(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

if __name__ == "__main__":
    main()
