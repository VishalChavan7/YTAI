# 📺 YouTube Transcript RAG

### AI-Powered Question-Answering for YouTube Videos

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-00A67E.svg)](https://openai.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ask questions about any YouTube video using AI. This project automatically fetches transcripts, handles English/Hindi language fallback, and uses RAG (Retrieval-Augmented Generation) to answer your questions accurately.

---

## 🎯 Overview

**YouTube Transcript RAG** is an intelligent question-answering system that:

1. **Fetches** YouTube video transcripts (English with Hindi fallback)
2. **Translates** Hindi transcripts to English using GPT-4o-mini
3. **Chunks** the transcript into semantic segments
4. **Embeds** chunks using OpenAI embeddings
5. **Stores** vectors in FAISS for fast retrieval
6. **Answers** your questions using context-aware AI

### Powered By

- **YouTube Transcript API** - Transcript extraction
- **LangChain** - RAG pipeline orchestration
- **OpenAI GPT-4o-mini** - Translation & Q&A
- **FAISS** - Vector similarity search
- **OpenAI Embeddings** - text-embedding-3-small

---

## ✨ Features

### 🌐 Smart Language Handling
- Automatically tries **English** transcripts first
- Falls back to **Hindi** if English unavailable
- Translates Hindi → English with high accuracy
- Gracefully handles videos without captions

### 🤖 Advanced RAG Pipeline
- **Recursive text splitting** (1000 chars, 200 overlap)
- **Semantic search** with OpenAI embeddings
- **Top-4 retrieval** for context-aware answers
- **Grounded responses** (answers only from transcript)

### 💬 Interactive Q&A
Ask unlimited questions like:
- *"What is the main topic of this video?"*
- *"Summarize the key points discussed."*
- *"What does the speaker say about [specific topic]?"*
- *"Explain the section between 5-10 minutes."*

---

## 🏗️ Project Structure

```
youtube-transcript-rag/
│
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not committed)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- pip package manager

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/youtube-transcript-rag.git
cd youtube-transcript-rag
```

**2. Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

⚠️ **Security Note:** Never commit your `.env` file. Add it to `.gitignore`.

---

## 📖 Usage

### Running the Application

```bash
python app.py
```

### Example Session

```
Enter YouTube Video ID: eNgD1kg3U14
English transcript found.
Using English transcript directly…
Total chunks created: 42
Vector store ready.

🎤 Ask anything about the video (type 'exit' to quit)
------------------------------------------------------

Your question: What is the main topic?

🧠 Answer:
The video discusses the fundamentals of machine learning,
focusing on supervised and unsupervised learning techniques...

Your question: exit
👋 Exiting…
```

### Finding the Video ID

The Video ID is the alphanumeric code after `v=` in the YouTube URL:

```
https://www.youtube.com/watch?v=eNgD1kg3U14
                                 ^^^^^^^^^^^
                                 Video ID
```

---

## 🧠 How It Works

### 1. Transcript Fetching

```python
# Try English first
yt.fetch(video_id, languages=["en"])

# Fallback to Hindi if needed
yt.fetch(video_id, languages=["hi"])
```

### 2. Translation (if Hindi)

Uses GPT-4o-mini to translate the entire transcript:
- Line-by-line accuracy
- No summarization
- Natural English output

### 3. Vectorization Pipeline

- **Split:** RecursiveCharacterTextSplitter (1000 chars)
- **Embed:** OpenAI text-embedding-3-small
- **Store:** FAISS vector database

### 4. Question Answering

- **Retrieval:** Top-4 most relevant chunks
- **Context:** Only uses transcript information
- **Response:** Grounded, factual answers

---

## 📦 Dependencies

```txt
python-dotenv        # Environment variable management
youtube-transcript-api  # Transcript fetching
langchain-openai     # OpenAI integration
langchain-text-splitters  # Text chunking
langchain-community  # FAISS support
faiss-cpu            # Vector search
tiktoken             # Token counting
requests             # HTTP requests
numpy                # Numerical operations
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |

### Model Settings

- **Translation:** `gpt-4o-mini` (temperature: 0)
- **Q&A:** `gpt-4o-mini` (temperature: 0.2)
- **Embeddings:** `text-embedding-3-small`
- **Chunk Size:** 1000 characters
- **Chunk Overlap:** 200 characters
- **Retrieval Count:** 4 chunks

---

## 🛡️ Important Notes

- ✅ Requires videos with **English or Hindi captions**
- ✅ API key must be valid and have sufficient credits
- ✅ Conversations are **not stored** (ephemeral)
- ✅ Translation may take 30-60 seconds for long videos
- ⚠️ Does not work with auto-generated captions (currently)

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas for improvements:

### Potential Enhancements
- 🌍 Support for more languages (Spanish, French, German)
- 🎨 Streamlit/Gradio web interface
- 🔗 Direct YouTube URL parsing
- 📊 Video summarization mode
- 💾 Conversation history storage
- 🚀 Batch processing for multiple videos
- 🎯 Timestamp-aware responses

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the RAG framework
- [OpenAI](https://openai.com/) for GPT and embeddings
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [FAISS](https://github.com/facebookresearch/faiss) for efficient vector search

---

## 📧 Contact

**Questions or suggestions?** Feel free to:
- Open an [issue](https://github.com/<your-username>/youtube-transcript-rag/issues)
- Submit a [pull request](https://github.com/<your-username>/youtube-transcript-rag/pulls)
- Reach out via email: your.email@example.com

---

## ⭐ Support

If this project helped you, please consider:
- Giving it a **star** ⭐ on GitHub
- Sharing it with others who might find it useful
- Contributing improvements or bug fixes

---

**Made with ❤️ and Python**
