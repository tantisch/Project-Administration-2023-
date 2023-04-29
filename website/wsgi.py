from src import create_app, connect_to_database

if __name__ == '__main__':
    connect_to_database()
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
