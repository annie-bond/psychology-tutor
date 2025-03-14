# Psychology Tutor

This project is designed to be a tool for A Level Psychology students that uses RAG. It scrapes a psychology A Level revision website and converts the content into text chunks with embeddings. It combines the most relevant pieces with an LLM to generate answers to psychology questions.


Description of files inside:
- webscraper.py: gathers data from the psychology website
- embeddings_creator: creates the FAISS vector store with embeddings and csv file storing the text
- faiss.index: already created vector store
- text_chunks.csv: already created text chunk store
- PsychologyTutorGPU.ipynb: a file to run in google colab that uses a memory intensive language model (13B parameters)
- PsychologyTutorCPU.ipynb: a file to run in google colab that uses a more lightweight model: (135M parameters)
