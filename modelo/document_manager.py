from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import threading
from repository import add

def run_in_separated_thread(arg, fun):
    print("Iniciando adição ao DB.")
    thread = threading.Thread(target=fun, args=(arg,))
    thread.start()
    return thread

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

# Configuração do loader com codificação
loader_txt = DirectoryLoader(
    './data/txt',
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'autodetect_encoding': True},
    use_multithreading=True,
    show_progress=True
)

try:
    documents = loader_txt.load()
    # Exibir documentos carregados para debug
    for doc in documents:
        print(f"Carregado: {doc.metadata['source']} - {len(doc.page_content)} caracteres")
    
    chunks = split_documents(documents)
    print(f"Chunks gerados: {len(chunks)}")
    
    # Iniciar thread
    new_thread = run_in_separated_thread(chunks, add)
    new_thread.join()

except Exception as e:
    print(f"Erro ao carregar ou processar documentos: {e}")