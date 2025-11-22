import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY missing. Add it to your .env file.")


# Fetch transcript (EN → HI fallback)
def fetch_transcript(video_id: str):
    yt = YouTubeTranscriptApi()
    transcript = ""
    lang = None

    # Try English first
    try:
        data = yt.fetch(video_id, languages=["en"])
        raw = data.to_raw_data()
        transcript = " ".join(x["text"] for x in raw)
        lang = "en"
        print("English transcript found.")
    except Exception:
        print("English transcript not available.")

    # If EN failed, try Hindi
    if not transcript:
        try:
            data = yt.fetch(video_id, languages=["hi"])
            raw = data.to_raw_data()
            transcript = " ".join(x["text"] for x in raw)
            lang = "hi"
            print("Hindi transcript found.")
        except Exception:
            pass

    if not transcript:
        raise RuntimeError("❌ No English/Hindi captions available for this video.")

    return transcript, lang


# Translate Hindi → English (if needed)
def translate_if_hindi(text: str, lang: str) -> str:
    if lang != "hi":
        print("Using English transcript directly…")
        return text

    print("Translating Hindi → English. This may take a while…")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = f"""
    Translate the following Hindi transcript to English.
    Do not summarize, translate fully and accurately.

    {text}
    """

    translated = llm.invoke(prompt).content
    print("Translation completed.")
    return translated


# Build vector store
def build_vector_store(text: str) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])
    print(f"Total chunks created: {len(docs)}")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = FAISS.from_documents(docs, embeddings)
    print("Vector store ready.")
    return vs


def format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)


# MAIN
def main():
    video_id = input("Enter YouTube Video ID: ").strip()

    # 1. Fetch transcript (EN → HI)
    transcript, lang = fetch_transcript(video_id)

    # 2. Translate if needed
    text = translate_if_hindi(transcript, lang)

    # 3. Build Vector Store
    vector_store = build_vector_store(text)
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 4}
    )

    # Single LLM instance for Q&A
    qa_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    print("\n🎤 Ask anything about the video (type 'exit' to quit)")
    print("------------------------------------------------------")

    while True:
        q = input("\nYour question: ").strip()
        if q.lower() in ["exit", "quit", "bye"]:
            print("👋 Exiting…")
            break

        docs = retriever.invoke(q)
        context = format_docs(docs)

        prompt = f"""
        You are a helpful assistant.
        Use ONLY the transcript context to answer the user.
        If the answer is not present, reply: "I don't know from the transcript."

        Transcript:
        {context}

        Question: {q}
        """

        answer = qa_llm.invoke(prompt).content
        print("\n🧠 Answer:")
        print(answer)


if __name__ == "__main__":
    main()
