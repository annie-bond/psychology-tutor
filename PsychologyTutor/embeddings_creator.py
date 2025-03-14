import faiss
import numpy as np
import csv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import webcrawler

def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    print("number of chunks: ", len(chunks))
    return chunks


def generate_embeddings(chunks, embedding_model_name):
    encoder = SentenceTransformer(embedding_model_name)
    embeddings = encoder.encode(chunks)
    return embeddings

def create_faiss_index(embeddings, faiss_file_name):
    # convert embeddings numpy float32 format for faiss:
    embedding_array = np.array(embeddings, dtype=np.float32)
    print("embedding array shape: ", embedding_array.shape)

    # initialise database with the number of vector dimensions:
    d = embedding_array.shape[1]
    index = faiss.IndexFlatL2(d)

    # wrap database in IndexIDMap to store ids:
    index = faiss.IndexIDMap(index)

    # create 64-bit ids for faiss, insert with embeddings into index:
    ids = np.arange(embedding_array.shape[0]).astype(np.int64)
    index.add_with_ids(embedding_array, ids)

    # save in project:
    faiss.write_index(index, faiss_file_name)
    print(faiss_file_name, " created and saved")

def create_csv_file(chunks, csv_file_name):
    with open(csv_file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        writer.writerow(["id", "text_chunk"])
        for idx, chunk in enumerate(chunks):
            writer.writerow([idx, chunk])

    print(csv_file_name, " created and saved")


# function that does everything:
def create_embeddings_databases():
    webpages_text = webcrawler.crawl()
    chunks = chunk_text(webpages_text)
    embeddings = generate_embeddings(chunks, "BAAI/bge-small-en-v1.5")
    create_faiss_index(embeddings, "faiss.index")
    create_csv_file(chunks, "text_chunks.csv")


create_embeddings_databases()