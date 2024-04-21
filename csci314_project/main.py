from visualex import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # Run flask application, start webserver, say debug = true
    