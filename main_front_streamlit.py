'''
#NOUVELLE FONCTION CORRIGÉ 

import streamlit as st
import os
import asyncio
from pdf_parser import pdf_parser
from json_parser import json_parser  # Adjusted to the correct function name
from store_parsed_chunks import store_parsed_chunks

def save_uploaded_file(uploaded_file):
    try:
        file_path = os.path.join("uploaded_files", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write("File saved locally at:", file_path)
        return file_path
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

if not os.path.exists("uploaded_files"):
    os.mkdir("uploaded_files")
    st.write("Created directory for uploaded files.")

st.title("File Processor for Embeddings")
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'json'])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)
    
    saved_file_path = save_uploaded_file(uploaded_file)
    if saved_file_path:
        st.success("File saved successfully in the 'uploaded_files' folder.")
        
        course_id = st.text_input("Course ID", "Course123")
        resource_name = st.text_input("Resource Name", "Example Resource")
        resource_link = st.text_input("Resource Link", "http://example.com")

        metadata = {
            'course_id': course_id,
            'resource_name': resource_name,
            'resource_link': resource_link
        }

        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        if file_extension == '.pdf':
            # Process PDF file
            st.write("Parsing the PDF...")
            parsed_chunks_file, extracted_content = asyncio.run(pdf_parser(saved_file_path, metadata))
            st.text_area("Extracted Text", extracted_content, height=300)
            st.write("PDF parsing completed.")
            num_vectors_uploaded = asyncio.run(store_parsed_chunks(parsed_chunks_file))
        elif file_extension == '.json':
            # Process JSON file
            st.write("Parsing the JSON...")
            parsed_chunks_file, extracted_content = asyncio.run(json_parser(saved_file_path, metadata))
            st.text_area("Extracted Data", extracted_content, height=300)  # Adjust to show JSON data
            st.write("JSON parsing completed.")
            num_vectors_uploaded = asyncio.run(store_parsed_chunks(parsed_chunks_file))

        st.write(f"Number of vectors uploaded: {num_vectors_uploaded}")
        st.write("Data processing completed.")
    else:
        st.error("Failed to save the file.")
else:
    st.write("No file uploaded yet.")
'''

import streamlit as st
import os
import asyncio
from pdf_parser import pdf_parser
from json_parser import json_parser
from store_parsed_chunks import store_parsed_chunks

def save_uploaded_file(uploaded_file):
    try:
        file_path = os.path.join("uploaded_files", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write("File saved locally at:", file_path)
        return file_path
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

if not os.path.exists("uploaded_files"):
    os.mkdir("uploaded_files")
    st.write("Created directory for uploaded files.")

st.title("File Processor for Embeddings")
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'json'])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)
    
    saved_file_path = save_uploaded_file(uploaded_file)
    if saved_file_path:
        st.success("File saved successfully in the 'uploaded_files' folder.")
        
        # Metadata handling is commented out as it's not required for JSON processing currently.
        # Uncomment and modify as needed for future requirements.
        # metadata = {
        #     'course_id': st.text_input("Course ID", "Course123"),
        #     'resource_name': st.text_input("Resource Name", "Example Resource"),
        #     'resource_link': st.text_input("Resource Link", "http://example.com")
        # }

        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        if file_extension == '.pdf':
            # Process PDF file
            st.write("Parsing the PDF...")

            
            metadata = {  # Metadata is required for PDF parsing
                'course_id': 'Course123',
                'resource_name': 'Example Resource',
                'resource_link': 'http://example.com'
            }
            

            parsed_chunks_file, extracted_content = asyncio.run(pdf_parser(saved_file_path, metadata))
            st.text_area("Extracted Text", extracted_content, height=300)
            st.write("PDF parsing completed.")
            num_vectors_uploaded = asyncio.run(store_parsed_chunks(parsed_chunks_file))


        elif file_extension == '.json':
            # Process JSON file without passing metadata
            st.write("Parsing the JSON...")
            parsed_chunks_file, extracted_content = asyncio.run(json_parser(saved_file_path))
            st.text_area("Extracted Data", extracted_content, height=300)
            st.write("JSON parsing completed.")
            num_vectors_uploaded = asyncio.run(store_parsed_chunks(parsed_chunks_file))

        st.write(f"Number of vectors uploaded: {num_vectors_uploaded}")
        st.write("Data processing completed.")
    else:
        st.error("Failed to save the file.")
else:
    st.write("No file uploaded yet.")

