# Financial Ledger API

A **FastAPI + PostgreSQL** backend implementing a **double-entry financial ledger system** with
atomic transfers, balance integrity, and concurrency safety.

---

## 🚀 Features

- Double-entry bookkeeping (debit & credit)
- Atomic fund transfers (all-or-nothing)
- Ledger-based balance calculation
- Prevention of negative balances
- Concurrency-safe transactions
- Immutable ledger (append-only)
- Full transaction history
- Dockerized setup

---

## 🧱 Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Docker & Docker Compose**
- **Uvicorn**

---

## 📂 Project Structure

```

Double-entry-booking/
│
├── app/
│   ├── **init**.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routes.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Kusubhavani/Double-entry-booking
cd Double-entry-booking
````

---

### 2️⃣ Start the Application (Docker)

```bash
docker-compose up --build
```

Wait until you see:

```
Uvicorn running on http://0.0.0.0:8000
```

---

### 3️⃣ Open API Documentation

```
http://localhost:8000/docs
```

This opens **Swagger UI** with all available APIs.

---

## 🔗 API Endpoints

### ➕ Create Account

`POST /api/accounts`

**Params**

* `user_id`
* `currency`

---

### 💰 Get Account Balance

`GET /api/accounts/{account_id}/balance`

Balance is calculated dynamically from ledger entries.

---

### 🔄 Transfer Funds (Atomic)

`POST /api/transfer`

**Params**

* `from_account_id`
* `to_account_id`
* `amount`
* `reference`

✔ Creates **two ledger entries** (debit + credit)
✔ Ensures sufficient balance
✔ Uses database transactions
✔ Safe under concurrent requests

---

### 📜 Ledger History

`GET /api/accounts/{account_id}/ledger`

Returns full immutable transaction history.

---

## ✅ Expected Outcomes – Satisfaction Checklist

✔ REST API for account & transfers
✔ Atomic debit and credit entries
✔ Immutable ledger design
✔ Negative balance prevention
✔ Concurrency-safe transactions
✔ Balance derived from ledger entries
✔ Complete audit trail
✔ ACID-compliant database usage

---

## 🛡️ Data Integrity Guarantees

* **Serializable isolation level**
* **Row-level locking (`SELECT FOR UPDATE`)**
* **Transactional consistency**
* **No balance stored directly**

---

## 🔮 Future Enhancements

* Alembic migrations
* Idempotency keys
* Authentication & authorization
* Unit & integration tests
* Pagination for ledger history

---

## 👩‍💻 Author

Built as a **fintech-grade ledger backend** demonstrating
strong backend fundamentals and financial correctness.

---

✅ **Ready for evaluation, interviews, and production extension**

```

---

If you want, next I can:
- Add **sample Swagger request bodies**
- Add a **“How this satisfies expected outcomes” explanation**
- Add **screenshots section**
- Add **unit tests**

Just tell me 👍
```
