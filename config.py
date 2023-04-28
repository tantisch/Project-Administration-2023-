import os

secret_key = "very cool secret key"
connect_vc = {'host': os.getenv("DB_HOST"),
              'port': int(os.getenv("DB_PORT")),
              'user': 'dbadmin',
              'password': '',
              'database': 'VMart'
              }
