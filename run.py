from app import create_app
from livereload import Server

app = create_app()

@app.route('/')
def home():
    return "Home Page"

@app.route('/about')
def about():
    return "About Page"

@app.route('/user/<name>')      # Dynamic route
def user(name):
    return f"Hello, {name}!"

@app.route('/number/<int:num>') # Type conversion
def number(num):
    return f"Number is: {num}"

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    
    # Watch templates and static files
    server.watch('app/templates/')
    server.watch('app/static/')
    server.serve(port=5000, debug=True)

    # app.run(debug=True)
