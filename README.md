# AI Document Editor

## Description

This Streamlit-based application leverages the OpenAI API to provide functionalities such as document proofreading, heading generation, quote extraction, title and lead proposition, and tagging. The application is designed to handle `.docx` files, providing a comprehensive toolkit for editing and enhancing document content.

## Features

- **Document Reading**: Load and read content from DOCX files.
- **Text Chunking**: Break documents into manageable chunks.
- **Proofreading**: Correct grammatical, punctuation, and stylistic errors.
- **Heading Generation**: Automatically generate headings for sections.
- **Quote Extraction**: Extract significant quotes from the text.
- **Title and Lead Generation**: Propose engaging titles and leads based on the content.
- **Tagging**: Create and assign relevant tags to sections of the document.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JaremaPiekutowski/ai-editor-v2.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd ai-editor-v2
   ```
3. **Install dependencies**:
   ```bash
   poetry install
   ```

## Setup

- Ensure that you have an OpenAI API key.
- Set the OpenAI API key in your environment variables or in an .env file:
  ```bash
  export OPENAI_API_KEY='your_api_key_here'
  ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and go to `http://localhost:8501`.
3. Upload a DOCX file using the provided file uploader.
4. Click on `Redaguj!` to start the document processing.

## Contributing

Contributions to the AI Document Editor are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

Specify the type of license under which your project is available. Common licenses for open source projects include MIT, GPL, and Apache.

## Acknowledgments

- Thanks to OpenAI for providing the API used in this project.
- Inspired by the potential of AI in automating content editing and proofreading.
