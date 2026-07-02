import pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536,
    api_key=settings.OPENAI_KEY
)


def chunk_data(data, chunk_size=256): # create chunk document
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=50)
    chunks = text_splitter.split_documents(data)
    return chunks


def insert_or_fetch_embeddings(index_name, chunks, namespace):
    vector_store = PineconeVectorStore.from_documents(
        chunks,
        embeddings,
        index_name=index_name,
        namespace=namespace
    )
    logger.info(f"Embeddings inserted in namespace {namespace}")
    return vector_store


def get_vector_store(index_name: str, namespace: str):
    pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        dimensions=1536,
        api_key=settings.OPENAI_KEY
    )
    return PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings,
        namespace=namespace
    )


def delete_pinecone_namespace(index_name: str, namespace: str) -> None:
    pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY)
    index = pc.Index(index_name)
    index.delete(delete_all=True, namespace=namespace)
    logger.info(f"Deleted namespace {namespace} from index {index_name}")

