import streamlit as st
import fitz  # PyMuPDF
from docx import Document as DocxDocument

# Load pre-trained model and tokenizer
from transformers import MarianTokenizer, MarianMTModel

# Load pre-trained model and tokenizer
model_name = "Helsinki-NLP/opus-mt-en-hi"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

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
            # Tokenize and encode the input text
            input_ids = tokenizer.encode(input_text, return_tensors="pt")

            # Generate translation
            translation_ids = model.generate(input_ids)

            # Decode the translated text
            translated_text = tokenizer.decode(translation_ids[0], skip_special_tokens=True)

            # Display the translation
            st.subheader("Translated text in Hindi:")
            st.write(translated_text)

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

                # Tokenize and encode the input text
                input_ids = tokenizer.encode(text, return_tensors="pt")

                # Generate translation
                translation_ids = model.generate(input_ids)

                # Decode the translated text
                translated_text = tokenizer.decode(translation_ids[0], skip_special_tokens=True)

                # Display the translation
                st.subheader("Translated text in Hindi:")
                st.write(translated_text)

def extract_text_from_pdf(file_path):
    # Extract text from a PDF file using PyMuPDF
    text = ""
    with fitz.open(file_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            try:
                # Use try-except to handle potential IndexError
                text += pdf_document[page_num].get_text()
            except IndexError:
                # Handle the IndexError gracefully (e.g., print a message)
                print(f"Warning: IndexError on page {page_num}")
                print(f"Total number of pages in the PDF: {pdf_document.page_count}")
                break  # Exit the loop if an IndexError occurs
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
