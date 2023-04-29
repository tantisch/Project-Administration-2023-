import os

secret_key = "very cool secret key"
connect_postgres = {'host': os.getenv("DB_HOST"),
                    'port': int(os.getenv("DB_PORT")),
                    'user': 'postgres',
                    'password': 'postgres',
                    'database': 'postgres'
                    }
