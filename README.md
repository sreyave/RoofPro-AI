# 🏠 RoofPro AI – Smart Roofing Assistant

🚀 **RoofPro AI** is an intelligent, production-ready AI chatbot designed for roofing businesses. It provides real-time assistance for customer queries, emergency guidance, and cost estimation—while automatically capturing leads for business growth.

Built using **Flask + OpenAI + RAG (Retrieval-Augmented Generation)**, this project demonstrates how to combine AI with real-world business workflows.

---

## ✨ Features

- 🤖 **AI Chatbot** – Handles roofing-related queries intelligently  
- 📄 **RAG-Based Knowledge System** – Answers powered by custom PDF data  
- 🚨 **Emergency Repair Guidance** – Instant help for urgent roofing issues  
- 📐 **Cost Estimation** – Provides rough repair/replacement estimates  
- 📊 **Lead Capture System** – Stores user details directly in Google Sheets  
- 🔐 **Admin Dashboard** – View and manage incoming leads  
- 🌐 **Responsive UI** – Clean frontend using HTML, CSS, JS  

---

## 🧠 How It Works

1. User interacts with chatbot  
2. Query is processed using OpenAI  
3. Relevant knowledge is retrieved from PDF (RAG)  
4. AI generates a contextual response  
5. User details are captured as leads (if required)  
6. Leads are stored in Google Sheets  

---

## 🏗️ Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Backend     | Flask (Python) |
| AI Model    | OpenAI GPT + Embeddings |
| RAG Engine  | FAISS + PDF Processing |
| Database    | Google Sheets (gspread API) |
| Frontend    | HTML, CSS, JavaScript |
| Deployment  | Render |

---

## 📂 Project Structure

```
roofing_chatbot/
│
├── app/
│ ├── routes/ # Flask routes
│ ├── services/ # AI, RAG, Google Sheets logic
│ ├── templates/ # HTML pages
│ ├── static/ # CSS & JS
│ └── utils/
│
├── knowledge.pdf # Custom knowledge base
├── run.py # App entry point
├── requirements.txt
├── render.yaml
└── runtime.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/RoofPro-AI.git
cd RoofPro-AI
```

### 2️⃣ Create virtual environment
```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Add environment variables

Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CREDENTIALS=your_google_credentials_json_string
```
⚠️ Do NOT upload .env or credentials to GitHub

### 5️⃣ Run the app
```
python run.py
```
App will run on:
```
http://localhost:5000
```

### 🌍 Deployment (Render)
Add environment variables in Render dashboard:

- `OPENAI_API_KEY`
- `GOOGLE_CREDENTIALS`

Start command:
```
gunicorn run:app --bind 0.0.0.0:$PORT
```
---
## 🔐 Security Notes

- Never commit:
  - `credentials.json`
  - `.env`
- Always use environment variables in production  
- Rotate keys if exposed  

---

## 📌 Use Cases

- Roofing businesses 🏠  
- Local service providers 🛠️  
- AI chatbot projects 🤖  
- RAG-based applications 📄  

---

## 🚀 Future Improvements

- Database integration (PostgreSQL / MongoDB)  
- Multi-language support  
- Voice-based interaction  
- Advanced analytics dashboard  
- Vector DB (Pinecone / Weaviate)  

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

## 📄 License

This project is for educational and demonstration purposes.

## ⭐ Final Note

This project showcases how to build a real-world AI application that combines:

✔ Conversational AI
✔ Knowledge Retrieval (RAG)
✔ Lead Generation
✔ Cloud Deployment

## 📝 Author
Sreya Dhar