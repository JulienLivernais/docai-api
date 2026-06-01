from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
import logging


logger = logging.getLogger(__name__)


async def ask_and_get_answer(vector_store, query):
    llm = ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0.5,
        max_tokens=500,
        api_key=settings.OPENAI_KEY
    )

    retriever = vector_store.as_retriever(
        search_type='similarity_score_threshold',
        search_kwargs={'score_threshold': 0.5, 'k': 5}
    )

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based on the context below.
    If the answer is not in the context, say "I don't know based on the provided document."

    Context: {context}
    Question: {question}
    """)

    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    chain = prompt | llm | StrOutputParser()

    logger.info(f"Retrieved {len(docs)} chunks for query: {query}")

    return await chain.ainvoke({"context": context, "question": query})

