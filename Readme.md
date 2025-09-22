# Sweet Shop Management System – Backend

This is the backend API for the **Sweet Shop Management System**. It provides RESTful endpoints for user authentication, sweets management, and inventory control. The backend is containerized with Docker and uses PostgreSQL and MongoDB for persistence.

---

##  Features

* **User Authentication** (JWT-based)
* **Sweets Management**: add, list, update, delete sweets
* **Inventory Management**: purchase and restock sweets
* **Database Support**:

  * PostgreSQL (Auth + Inventory)
  * MongoDB (Products & catalog)

---

## 🐳 Run with Docker Compose

### 1. Clone the repo

```bash
git clone https://github.com/your-username/sweetshop-backend.git
cd sweetshop-backend
```

### 2. Start containers

```bash
docker-compose up -d
```

This will start:

* `auth-db` (Postgres, port 5433)
* `inventory-db` (Postgres, port 5434)
* `mongo` (MongoDB, port 27017)
* (Optional) your backend service container

### 3. Verify running services

```bash
docker ps
```

You should see all three containers up and running.

---

## 🔑 Connection Strings

* **Auth DB (Postgres)**
  `postgresql://auth_user:auth_pass@localhost:5433/auth_db`

* **Inventory DB (Postgres)**
  `postgresql://inventory_user:inventory_pass@localhost:5434/inventory_db`

* **MongoDB**
  `mongodb://root:example@localhost:27017/?authSource=admin`

---

## ▶️ Run Backend Locally (without Docker)

If you prefer running the backend API outside of Docker (e.g., with FastAPI, Django, or Node.js):

1. Create a `.env` file:

```env
AUTH_DB_URL=postgresql://auth_user:auth_pass@localhost:5433/auth_db
INVENTORY_DB_URL=postgresql://inventory_user:inventory_pass@localhost:5434/inventory_db
MONGO_URL=mongodb://root:example@localhost:27017/?authSource=admin
JWT_SECRET=supersecretkey
```

2. Install dependencies & start your backend service.

---

## 🧪 Testing

* Run unit and integration tests with:

```bash
pytest -v
```

* Ensure containers are running before executing tests.

---

## 📂 Project Structure (backend only)

```
backend/
  ├── src/
  │   ├── auth/        # authentication service
  │   ├── sweets/      # sweets management
  │   ├── inventory/   # inventory logic
  │   └── main.py      # entrypoint (FastAPI/Django/etc.)
  ├── tests/           # unit & integration tests
  ├── docker-compose.yml
  └── README.md
```

---

## 🤖 My AI Usage

I used AI tools (ChatGPT, Copilot, etc.) to:

* Generate initial boilerplate for `docker-compose.yml`
* Debug connection/authentication issues for MongoDB and Postgres
* Write documentation (this README)

**Reflection:** AI sped up setup and saved time debugging DB connection issues. I still validated and tested all generated code manually.

---

##

---

##
