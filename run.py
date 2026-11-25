from app import create_app

app = create_app()
port=5269

if __name__ == '__main__':
    app.run(port=port, debug=True, use_debugger=False)
