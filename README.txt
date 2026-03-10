Laptop Hub Inventory

A simple full-stack laptop inventory management system built with
FastAPI, PostgreSQL, and React. The application allows users to manage
laptop products with full CRUD operations through a REST API and a React
frontend.

Features - Add new laptop products - View all products - Update product
details - Delete products - Product search, sorting, and filtering -
React frontend connected to FastAPI backend

Tech Stack

Backend - Python - FastAPI - SQLAlchemy - PostgreSQL - Pydantic

Frontend - React - Axios - HTML / CSS

Project Structure

project/ │ ├── main.py ├── database.py ├── database_model.py ├──
models.py │ └── frontend/ ├── src/ │ ├── App.js │ ├── index.js │ └──
components

Installation

1.  Clone Repository git clone cd project

2.  Install Backend Dependencies pip install fastapi uvicorn sqlalchemy
    psycopg2-binary

3.  Run Backend uvicorn main:app –reload

Backend runs on: http://localhost:8000

API Docs: http://localhost:8000/docs

4.  Run Frontend cd frontend npm install npm start

Frontend runs on: http://localhost:3000

API Example GET /products POST /product PUT /product/{id} DELETE
/product/{id}

Example Product: { “id”: 1, “name”: “Laptop”, “price”: 60000,
“description”: “High performance laptop”, “quantity”: 50 }

Author Aamir Ayub
