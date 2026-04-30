from app import create_app
from livereload import Server

app = create_app()

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    
    # Watch templates and static files
    server.watch('app/templates/')
    server.watch('app/static/')
    server.serve(port=5000, debug=True)

    # app.run(debug=True)
