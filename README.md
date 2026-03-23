# 🚀 Social Media Flask App

A scalable **Flask + TailwindCSS** web application using the application factory pattern and modular architecture.

---

# 📁 Project Structure

```
social_app/
│
├── app/
│   ├── __init__.py        # App factory
│   ├── models/            # Database models
│   ├── routes/            # Blueprints (user, profile, etc.)
│   ├── templates/         # Jinja2 templates
│   ├── static/
│   │   └── css/
│   │       ├── input.css
│   │       └── output.css
│
├── run.py                 # Entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── tailwind.config.js
├── package.json
├── .gitignore
```

---

# ⚙️ Setup Guide

## 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd social_app
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv env
```

Activate:

- Windows:
```bash
env\Scripts\activate
```

- Mac/Linux:
```bash
source env/bin/activate
```

---

## 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ (If requirements.txt not available)

Install manually:

```bash
pip install flask python-dotenv livereload
```

Then generate:

```bash
pip freeze > requirements.txt
```

---

## 5️⃣ Setup Tailwind CSS

### Install Node dependencies:

```bash
npm install
```

If not initialized:

```bash
npm init -y
npm install -D tailwindcss
npx tailwindcss init
```

---

## 6️⃣ Configure Tailwind

### tailwind.config.js

```js
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/**/*.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

---

## 7️⃣ Tailwind Input File

### app/static/css/input.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

# ▶️ Run Tailwind Watch (IMPORTANT)

```bash
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/output.css --watch
```

👉 Keeps CSS updated automatically during development

---

# ▶️ Run Flask Server

```bash
python run.py
```

OR

```bash
flask run --debug
```

---

# 🔥 Live Reload (Auto Refresh)

Using `livereload`:

- Auto refresh browser on:
  - HTML changes
  - CSS updates

Make sure `run.py` includes:

```python
from livereload import Server

server = Server(app.wsgi_app)
server.watch('app/templates/')
server.watch('app/static/')
server.serve(debug=True)
```

---

# 🌐 Access Application

```
http://127.0.0.1:5000/
```

---

# 💡 Development Workflow

Run **two terminals**:

### Terminal 1 (Tailwind)

```bash
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/output.css --watch
```

### Terminal 2 (Flask)

```bash
python run.py
```

---

# 📦 Requirements Management

## Freeze dependencies

```bash
pip freeze > requirements.txt
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚠️ Notes

- Do NOT commit `.env`
- Do NOT commit `node_modules`
- Activate virtual environment before installing packages
- Keep Tailwind watcher running

---

# 🚀 Features

- Flask Application Factory
- Modular Blueprints
- TailwindCSS Integration
- Live Reload (auto refresh)
- Clean and scalable architecture

---

# 🔮 Future Improvements

- Authentication (Login/Register)
- PostgreSQL integration
- REST API
- Vue/Vite frontend integration

---

# 👨‍💻 Author

Md. Akkas Ali