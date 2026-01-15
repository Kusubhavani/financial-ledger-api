# Financial Ledger API

A basic FastAPI + PostgreSQL backend implementing a **double-entry financial ledger system**.

---

## 🚀 Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose

---

## 📂 Project Setup

1️⃣ Clone Repository

git clone https://github.com/Kusubhavani/financial-ledger-api.git

cd financial-ledger-api

2️⃣ Run with Docker
docker-compose up --build

3️⃣ API Docs

Open in browser:

http://localhost:8000/docs

🔗 Available APIs
Create Account

POST /api/accounts

Create Transaction

POST /api/transactions

Create Ledger Entry

POST /api/ledger-entry

## Expected Outcomes Satisfaction

✔ Atomic double-entry ledger  
✔ Debit + Credit per transfer  
✔ Ledger immutability  
✔ No negative balances  
✔ Concurrency safe (row locking + serializable isolation)  
✔ Balance derived from ledger entries  
✔ Complete transaction history  
✔ Database transactions ensure integrity  
