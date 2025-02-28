# FUNÇÕES PRIMÁRIAS
import threading

# LOAD DATA
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, BSHTMLLoader

# SPLIT DATA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

# REPOSITORY
from repository import add

# DEFINE OUTROS THREADS
def run_in_separated_thread(arg, fun):
    print("Iniciando adição ao DB.")
    thread = threading.Thread(target=fun, args=(arg,))
    thread.start()
    return thread

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 80,
        length_function = len,
        is_separator_regex=False
    )

    return text_splitter.split_documents(documents)

loader = DirectoryLoader('./data/txt', glob="**/*.txt", loader_cls=TextLoader, use_multithreading=True, show_progress=True).load()
loader += DirectoryLoader('./data/pdf', glob="**/*.pdf", loader_cls=PyPDFLoader, use_multithreading=True, show_progress=True).load()
loader += DirectoryLoader('./data/html', glob="**/*.html", loader_cls=BSHTMLLoader, use_multithreading=True, show_progress=True).load()

chunks = split_documents(loader)
print(chunks)

new_thread = run_in_separated_thread(chunks, add)
new_thread.join()