Project/
├── backend/
│   ├── models/
│   │   ├── transaction.py         # Transaction model
│   │   ├── user.py                # User model
│   │   └── run_tables.py          # Table creation script
│   ├── routers/
│   │   └── auth.py                # Auth endpoints
│   ├── schema/
│   │   └── auth.py                # Pydantic schemas
│   ├── services/
│   │   └── auth_service.py        # Auth service layer
│   ├── config.py                  # App configuration loader
│   ├── database.py                # Database connection
│   ├── dependencies.py            # Shared FastAPI dependencies
│   ├── health.py                  # Health check logic
│   ├── main.py                    # FastAPI app entrypoint
│   └── utils.py                   # Helper utilities
├── .env                           # Environment variables (add manually)
├── .gitignore                     # Files ignored by Git
├── Dockerfile                     # Docker image definition (to be added)
├── docker-compose.yml             # Multi-container setup (to be added)
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation



Instructions to run project : Fin_Track
1. Pull the updated code from the project repository (fin-tracker-be).
2. Navigate to the project directory.
3. Install the same Python version : Python 3.10.11
4. Activate the virtual environment (env) using the command `source env/bin/activate`.
5. Install the required packages using pip.
6. (requirements.txt) Install the project using 
     - `pip install -r requirements.txt`
     - `pip install Sqlalchemy`
     - `pip install python-jose[cryptography]`
     - `pip install the bcrypt package`
7. Manually create the .env file in the root directory and add the following line:
8.  using PostgreSQL, recreate the DB and update credentials in .env.
    The DB Credentials are :
    DATABASE_URL : `private`
    SECRET_KEY : `Private`
    ALGORITHM=`HS256`
    ACCESS_TOKEN_EXPIRE_MINUTES=`30`
    FRONTEND_ORIGIN=`https://v0-fastapi-frontend-in-next-js.vercel.app/`

9. Run the backend API using `uvicorn backend.main:app --reload`
10. SwaggerUI : `127.0.0.1:8000/docs`


Message Zohaib Nizami





