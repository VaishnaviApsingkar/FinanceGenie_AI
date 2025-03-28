# 💰 FinanceGenie AI 

FinanceGenie AI is an intelligent financial assistant that helps users **manage their bank accounts, analyze transactions, and generate insights using AI**.  
Built with **Flask, SQLAlchemy, OpenAI, and OCR technologies**, it enables **smart financial decisions** through **AI-driven analysis**.

---

## 🔥 Features  

✅ **User Authentication** (Login, JWT-based security)  
✅ **Bank Account Management** (Add, Retrieve, Delete accounts)  
✅ **AI-Powered Querying** (Generate SQL queries using OpenAI)  
✅ **OCR-based File Processing** (Extract data from PDFs & images)  
✅ **Automated Transaction Summarization** (AI-driven insights using OpenAI GPT model)  

---

## 🏗️ Project Structure  
```
FinanceGenie-AI/
│── app/
│   ├── auth/                 # User authentication (Login, JWT)
│   ├── home/                 # Dashboard, transaction handling
│   ├── static/               # Frontend assets (CSS, JS, Images)
│   ├── templates/            # HTML templates for Flask
│   ├── models.py             # Database models (SQLAlchemy)
│── migrations/               # Database migrations
│── uploads/                  # Stores uploaded files
│── .env                      # Environment variables
│── config.py                 # Flask configuration
│── run.py                    # Main Flask app entry point
│── requirements.txt           # Python dependencies
│── README.md                  # Project documentation
```

---

## 🚀 Tech Stack  

| Technology  | Purpose |
|------------|---------|
| 🐍 Flask | Backend Framework |
| 🗄️ SQLAlchemy | ORM for database handling |
| 🔐 Flask-Login | User authentication |
| 🤖 OpenAI API | AI-powered query generation |
| 🏦 SQLite/PostgreSQL | Database for transactions |
| 🖼️ PIL (Pillow) | Image processing |
| 📝 Tesseract-OCR | Text extraction from images |
| 📄 pdfplumber | Text extraction from PDFs |

---

## 🎯 API Endpoints  

### 🔹 **Authentication**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/login` | User login |
| `POST` | `/api/register` | Register new user |

### 🔹 **Bank Account Management**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/get_accounts` | Fetch all bank accounts |
| `POST` | `/api/add_account` | Add a new bank account |
| `DELETE` | `/api/delete_account/<id>` | Delete an account |

### 🔹 **AI-Powered Queries**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/process_file_and_add_transaction` | AI-driven transaction analysis |

---
## 📸 Screenshots

<img src="https://github.com/VaishnaviApsingkar/FinanceGenie_AI/blob/bfe313c02a1b5f1bf5271c40ea6401b4279578aa/images/img1.png" alt="FinanceGenie Dashboard" width="600" height="300">

<img src="https://github.com/VaishnaviApsingkar/FinanceGenie_AI/blob/bfe313c02a1b5f1bf5271c40ea6401b4279578aa/images/img2.png" alt="FinanceGenie Dashboard" width="600" height="300">

<img src="https://github.com/VaishnaviApsingkar/FinanceGenie_AI/blob/966179ec06653c7bd43797ea926f76f2bd240723/images/img3.png" alt="FinanceGenie Dashboard" width="600" height="300">

<img src="https://github.com/VaishnaviApsingkar/FinanceGenie_AI/blob/966179ec06653c7bd43797ea926f76f2bd240723/images/img4.png" alt="FinanceGenie Dashboard" width="600" height="300">

---

Made with ❤️ by **Vaishnavi Pravin Apsingkar**



