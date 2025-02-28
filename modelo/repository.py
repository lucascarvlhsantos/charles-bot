# SUPORT LIBS
import os, re, threading

# SPLIT DATA
from langchain.schema.document import Document

# EMBEDDINGS
from langchain.embeddings.openai import OpenAIEmbeddings

# CREATE DATABASE
from langchain.vectorstores import Chroma

# FORMATADOR
from formarter import format_results, format_chunk_names

CHROMA_PATH = "database"

def add(chunks: list[Document]):
    ids = format_chunk_names(chunks)
    for pos, chunk in enumerate(chunks):
        chunk.metadata["id"] = ids[pos]
    
    embedding_fun = get_embedding_fun()
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_fun
    )

    db.add_documents(chunks, ids=ids)
    db.persist()

def existentes(db):
    existent = set(db.get(include=[]))
    print(len(existent))

def get_embedding_fun():
    # OPENAI EMBEDDINGS
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",  # Modelo recomendado para embeddings
    )
    return embeddings

def get_results(message):
    embedding_fun = get_embedding_fun()
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_fun
    )
    print("Iniciando busca das informações...")
    results = db.similarity_search_with_score(message, k=8)

    #results = results[::0]
    results = [(doc, 1 - score) for doc, score in results]
    max_score = results[0][1]
    ptr = 0

    print(f"MAX_SCORE: {max_score}")

    if max_score < 0.60:
        return {'content': "Não foi possível achar informações pertinentes.", 'fonts': ""} 

    for i, (doc, score) in enumerate(results):
        if score > max_score * 0.98:
            print(f"SCORE ACEITO: {score}")
            ptr = i
        else:
            print(f"SCORE REJEITADO: {score}")
            break

    results = results[0:ptr+1]

    print("Formatando resultados...")
    formated_results = format_results(results)

    return formated_results

existentes(Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_fun()
    ))